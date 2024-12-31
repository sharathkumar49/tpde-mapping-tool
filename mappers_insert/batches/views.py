
from .models import PrivateiAccMasterMapping, NTAccountMapping, ReportTemplates, Batches
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .function import get_report_details, get_model_name
from .serializers import MappersListSerializer, NTAccountListSerializer, BatchListSerializer
from masters.function import Validation, ExecuteSQLQuery
import pandas as pd
import numpy as np
from standard.variables import Variables, Queries
import pandas as pd
import numpy as np
from rest_framework import status, filters, generics
import json 
import operator
from django.db.models import Q
from functools import reduce
from datetime import datetime

variable_obj = Variables()

class Headers:
	"""
	Class to define headers for PrivateiAcc and NTAccounting.
	"""
	def __init__(self):
		self._privateiacc_header = ['ClientID', 'BurgissPortfolioName', 'InvestmentName',
									'InvestmentGUID', 'InvestmentID', 'UploadValuations',
									'UploadTransactions', 'PortfolioCode', 'PrimaryScope',
									'PrimaryFundCode', 'EntityType', 'CommitmentID', 'ClassID',
									'TrancheID', 'SecondaryLegScope', 'SecondaryLegCode',
									'Notes']
		self._ntaccounting_header = ['ClientID', 'Consolidation', 'NTAccountNumber',
									 'NTAccountName', 'CSecurityId', 'NSecNum', 'IsSMA',
									 'UploadValuationsDaily', 'UploadTransactionsDaily',
									 'UploadValuationsMonthly', 'UploadTransactionsMonthly',
									 'PortfolioCode', 'PortfolioName', 'PrimaryScope',
									 'PrimaryFundCode', 'PrimaryFundName', 'PrimaryFundType',
									 'CommitmentID', 'ClassID', 'TrancheID', 'SecondaryLegScope',
									 'SecondaryLegCode', 'TagDaily', 'TagMonthly', 'EntityType']

class StandardValidation:
	"""
	Class to perform standard validation on dataframes.
	"""
	def __init__(self):
		self.__upload_values = [0, 1]
		self.__fund = "fund"
		self.__cash = "cash"
		self.secondarylegscope_values = [self.__fund, self.__cash]
		self.primaryfundcode_cols = ['ClientID', 'PrimaryFundCode']
		self.portfoliocode_cols = ['ClientID', 'PortfolioCode']
		self.correct = "Correct"
		self.drawdown = "Drawdown"
		self.nondrawdown = "Non-Drawdown"
		self.hybrid = "Hybrid"
		self.header_class = Headers()

	def strip_whitespaces(self, df, headers):
		"""
		Strip whitespaces from the specified columns in the dataframe.
		"""
		for column in headers:
			df[column] = df[column].apply(lambda x: x.strip() if isinstance(x, str) else x)
		return df

	def integer_conversion(self, df, columns):
		"""
		Convert specified columns to integer, replacing invalid values with a default.
		"""
		for column in columns:
			df[column] = df[column].replace([np.inf, -np.inf, ''], np.nan).fillna(8634767364).astype(int)
		return df

	def revert_to_original(self, df, columns):
		"""
		Revert specified columns to their original values.
		"""
		for column in columns:
			df[column] = df[column].replace(8634767364, '')
		return df

	def client_id_empty_check(self, df, headers):
		"""
		Check for empty ClientID in the dataframe and handle errors.
		"""
		df['error_col'] = pd.isna(df['ClientID'])
		indices = np.where(df["error_col"])
		row_indices = indices[0]
		clientid_empty_df = pd.DataFrame()
		if len(row_indices) > 0:
			clientid_empty_df = pd.DataFrame(columns=headers)
			for indice in row_indices:
				record_to_append = df.iloc[indice]
				record_to_append['Error'] = True
				record_to_append['ErrorMessages'] = {'ClientID': variable_obj.error_messages['client_id_empty']}
				record_to_append['ClientID'] = ''
				record_to_append['DuplicateEntry'] = False
				clientid_empty_df = pd.concat([clientid_empty_df, pd.DataFrame([record_to_append])], ignore_index=True)
			df = df.drop(['error_col'], axis=1)
			df = df.drop(row_indices)
			clientid_empty_df = clientid_empty_df[headers + ["Error", "ErrorMessages"]]
		return {"main_df": df, "clientid_empty_df": clientid_empty_df}

	def client_id_valid_check(self, df):
		"""
		Validate ClientID against the database.
		"""
		db_client_ids = ExecuteSQLQuery(Queries()._client_details_query)
		print("\nDBClientIDs: ", db_client_ids.columns)
		df = df.merge(db_client_ids, on='ClientID', how='left')
		df['Check -> ClientID'] = df['ClientName'].apply(
			lambda x: variable_obj.error_messages['invalid_client_id'] if pd.isnull(x) else '')
		return df

	def upload_transactions_and_valuations_check(self, df, columns):
		"""
		Check upload transactions and valuations for specified columns.
		"""
		for col in columns:
			df['Check -> ' + col] = df[col].apply(lambda x: variable_obj.error_messages['invalid_uploadvaluation'] if x not in self.__upload_values else variable_obj.empty)
		return df

	def secondarylegscope_check(self, df):
		"""
		Check SecondaryLegScope values in the dataframe.
		"""
		df['SecondaryLegScope'] = df['SecondaryLegScope'].fillna(variable_obj.empty)
		df['Check -> SecondaryLegScope'] = df['SecondaryLegScope'].apply(
			lambda x: variable_obj.error_messages['invalid_secondarylegscope'] if x.lower() not in self.secondarylegscope_values else variable_obj.empty)
		return df

	def secondarylegcode_check(self, df):
		"""
		Check SecondaryLegCode values in the dataframe.
		"""
		df['SecondaryLegCode'] = df['SecondaryLegCode'].fillna(variable_obj.empty)
		print(df['SecondaryLegCode'])
		df['Check -> SecondaryLegCode'] = df['SecondaryLegCode'].apply(
			lambda x: variable_obj.error_messages['invalid_secondarylegcode'] if x.lower() == self.__fund and x == np.nan else variable_obj.empty)
		return df

	def primaryfundcode_check(self, df):
		"""
		Check PrimaryFundCode values against the database.
		"""
		db_fund_ids = ExecuteSQLQuery(Queries()._fund_details_query)
		df = df.merge(db_fund_ids, on=self.primaryfundcode_cols, how='left')
		df['Check -> FundCode'] = df.apply(lambda x: variable_obj.error_messages['invalid_primaryfundcode'] if pd.isnull(x['PrimaryUserFundID']) else '', axis=1)
		return df

	def portfoliocode_check(self, df):
		"""
		Check PortfolioCode values against the database.
		"""
		db_portfolio_ids = ExecuteSQLQuery(Queries()._portfolio_details_query)
		df = df.merge(db_portfolio_ids, on=self.portfoliocode_cols, how='left')
		df['Check -> PortfolioCode'] = df.apply(
			lambda x: variable_obj.error_messages['invalid_portfoliocode']
			if pd.isnull(x['UserPortfolioID']) else '', axis=1)
		return df

	def commitmentid_check(self, df):
		"""
		Check CommitmentID values against the database.
		"""
		client_ids = tuple(df['ClientID'].unique())
		print(len(client_ids), "client ids")
		client_str = "({})"
		if len(client_ids) == 1:
			client_ids = client_str.format(client_ids[0])
		query = Queries()._commitments_details_query.format(self.correct, client_ids)
		result = ExecuteSQLQuery(query)
		cols = ['ClientID', 'PrimaryFundCode', 'PortfolioCode', 'CommitmentID']
		df = df.merge(result, on=cols, how='left')

		df['Check -> CommitmentID'] = df['Check'].apply(lambda x: '' if x == self.correct else variable_obj.error_messages['invalid_commitmentid'])
		return df

	def classid_check(self, df):
		"""
		Check ClassID values against the database.
		"""
		client_ids = tuple(df['ClientID'].unique())
		client_str = "({})"
		if len(client_ids) == 1:
			client_ids = client_str.format(client_ids[0])
		query = Queries().userclass_details_query.format(self.correct, client_ids)
		result = ExecuteSQLQuery(query)
		df = df.merge(result, on=['ClientID', 'PrimaryFundCode', 'ClassID'], how='left')

		df['Check -> ClassID'] = df.apply(lambda x: variable_obj.error_messages['invalid_classid'] if pd.isnull(x['ClassIDCheck']) and x['EntityType'] == self.nondrawdown else '', axis=1)
		return df

	def duplicate_check_models(self, request, data, columns):
		"""
		Check for duplicate records in the specified model.
		"""
		model = get_model_name(request)
		print(model)
		ret_data = []
		for record in data:
			print("\n\n\nfalse\n\n\n")
			params = {x: record[x] if str(record[x]) != 'nan' else '' for x in columns}
			print(params)
			model_obj = model.objects.filter(**params)
			if len(model_obj) == 0:
				ret_data.append(record)
		print(ret_data)
		return ret_data

	@staticmethod
	def fillna(df, headers):
		"""
		Fill NaN values in the specified columns with a default value.
		"""
		for header in headers:
			df[header] = df[header].fillna(variable_obj.empty)
		return df

	@staticmethod
	def quotation_replace(df, headers):
		"""
		Replace single quotes with double quotes in the specified columns.
		"""
		for header in headers:
			df[header] = df[header].str.replace("'", '"')
		return df

	@staticmethod
	def check_column_create(headers):
		"""
		Create check columns for the specified headers.
		"""
		return ["Check -> {}".format(header) for header in headers]

	@staticmethod
	def check_blank_column(row, non_blank_columns):
		"""
		Check for blank columns in the specified row.
		"""
		null_columns = [col for col in non_blank_columns if (pd.isnull(row[col]) or pd.isna(row[col]))]
		return null_columns if null_columns else variable_obj.empty

	@staticmethod
	def check_duplicate_rows(df: pd.DataFrame, columns: list) -> pd.DataFrame:
		"""
		Check for duplicate rows in the dataframe based on the specified columns.
		"""
		s = df[columns].duplicated()
		df = pd.concat([df, s.rename("duplicated_entry_bool")], axis=1)
		df['DuplicateEntry'] = df["duplicated_entry_bool"].apply(
			lambda x: True if x else False)
		df = df.drop(['duplicated_entry_bool'], axis=1)
		return df

	@staticmethod
	def error_bool(row, checkcolumns):
		"""
		Check if there are any errors in the specified columns of the row.
		"""
		for col in checkcolumns:
			if row[col]:
				return True
		return False

	@staticmethod
	def error_dict(row, checkcolumns):
		"""
		Create a dictionary of errors for the specified columns of the row.
		"""
		error_columns = {}
		for col in checkcolumns:
			if col == 'Check -> BlankColumns':
				if row[col]:
					for key in row[col]:
						error_columns.update({key: f'{key} cannot be blank'})
			else:
				if row[col]:
					error_columns.update({str(col.split('->')[1]).strip(): row[col]})
		return error_columns
	

class DataValidation(APIView):
	"""
	DataValidation class handles the validation and insertion of data.

	Methods:
	- __init__: Initializes the DataValidation class.
	- get_header: Retrieves the header from the request.
	- mappers_insert: Inserts data into the mappers table after validation.
	- nt_account_mapping: Maps NT accounts after validation.
	"""

	def __init__(self) -> None:
		"""
		Initializes the DataValidation class.
		"""
		self.header_class = Headers()
		self.validation_obj = StandardValidation()
		self.header = ''
		self.exception_message = ''

	def get_header(self, request):
		"""
		Retrieves the header from the request.

		Args:
		- request: The HTTP request object.

		Returns:
		- header: The header list.
		"""
		template_obj = ReportTemplates.objects.filter(FeedID=request.POST.get('FeedID'), FeedCategoryID=request.POST.get('FeedCategoryID'), Active=1)
		self.header = template_obj[0].TemplateHeaders.split(',')
		self.header = [x.strip() for x in self.header]
		return self.header

	def mappers_insert(self, request, *args, **kwargs):
		"""
		Inserts data into the mappers table after validation.

		Args:
		- request: The HTTP request object.
		- args: Additional arguments.
		- kwargs: Additional keyword arguments.

		Returns:
		- Response: The HTTP response object.
		"""
		self.get_header(request)
		request_data = []
		duplicate_check = True
		if len(kwargs) > 0:
			request_data = kwargs['data']
			self.header.insert(0, 'MappingID')
			duplicate_check = False
		else:
			filename = request.FILES['data_file']
			main_df = pd.read_csv(filename, encoding_errors='ignore')
			request_data = main_df.to_dict('records')
		duplicate_comb_check = ['ClientID', 'BurgissPortfolioName',
					'InvestmentName', 'InvestmentGUID',
					'InvestmentID', 'PortfolioCode',
					'PrimaryFundCode']
		if duplicate_check:
			request_data = self.validation_obj.duplicate_check_models(request, request_data, duplicate_comb_check)
		if len(request_data) == 0:
			return Response(request_data)
		main_df = pd.DataFrame(request_data, columns=self.header)
		if 'Notes' not in main_df.columns:
			main_df['Notes'] = variable_obj.empty
		main_df = main_df[self.header]
		main_df = self.validation_obj.integer_conversion(main_df, ['ClientID', 'UploadTransactions', 'UploadValuations'])
		numeric_value_columns = {'ClientID', 'InvestmentID', 'UploadValuations',
						'UploadTransactions'}
		whitespace_strip_headers = [header for header in self.header if header not in numeric_value_columns]        
		main_df = self.validation_obj.strip_whitespaces(main_df, whitespace_strip_headers)
		ret_dict = self.validation_obj.client_id_empty_check(main_df,self.header)
		main_df = ret_dict['main_df']
		clientid_empty_df = ret_dict['clientid_empty_df']
		
		main_df = self.validation_obj.check_duplicate_rows(main_df, duplicate_comb_check) 
		# Check for Valid ClientID
		main_df = self.validation_obj.client_id_valid_check(main_df)
		main_df['ClientID'] = main_df['ClientID'].astype(int)
		main_df = self.validation_obj.upload_transactions_and_valuations_check(main_df, ['UploadTransactions', 'UploadValuations'])

		# non blank columns -> Source data columns that cannot be left blank
		non_blank_columns = {'BurgissPortfolioName','InvestmentName','InvestmentGUID'}
		main_df['Check -> BlankColumns'] = main_df.apply(
			self.validation_obj.check_blank_column, axis=1, non_blank_columns=non_blank_columns)

		# SecondaryLegScope and SecondaryLegCode check
		main_df = self.validation_obj.secondarylegscope_check(main_df)
		main_df = self.validation_obj.secondarylegcode_check(main_df)

		# Check Fund Code and Fund ID
		main_df = self.validation_obj.primaryfundcode_check(main_df)
			
		# Check Portfolio Code
		main_df = self.validation_obj.portfoliocode_check(main_df)
		main_df = self.validation_obj.fillna(main_df, ["PrimaryFundType", "ClassID", "CommitmentID", "TrancheID", "SecondaryLegCode"])
		main_df = self.validation_obj.quotation_replace(main_df, ["BurgissPortfolioName", "InvestmentName", "PortfolioName", "PrimaryFundName"])
		print (main_df['PrimaryFundType'])
		main_df['EntityType'] = main_df['PrimaryFundType'].apply(lambda x : 'Drawdown' if str(x)=="Drawdown" or "Hybrid" in x else 'Non-Drawdown')
		print (main_df['PrimaryFundType'])
		main_df = self.validation_obj.commitmentid_check(main_df)
		main_df = self.validation_obj.classid_check(main_df)
		
		cols = ['ClientID', 'UploadTransactions', 'UploadValuations', 'BlankColumns', 'SecondaryLegScope', 'SecondaryLegCode', 'FundCode', 'PortfolioCode', 'CommitmentID', 'ClassID']
		column_to_validate = self.validation_obj.check_column_create(cols)

		main_df['Error'] = main_df.apply(self.validation_obj.error_bool, axis=1,
										checkcolumns=column_to_validate)

		main_df['ErrorMessages'] = main_df.apply(self.validation_obj.error_dict, axis=1,
												checkcolumns=column_to_validate)
		main_df = self.validation_obj.revert_to_original(main_df, ['ClientID', 'UploadTransactions', 'UploadValuations'])
		result_cols = self.header + ['FundCurrency', 'DuplicateEntry', 'Error', 'ErrorMessages']
		main_df = main_df[result_cols]
		if clientid_empty_df.empty:
			result_df = main_df
		else:
			result_df = pd.DataFrame.from_dict(main_df.to_dict('records') + clientid_empty_df.to_dict('records'))
		result_df = self.validation_obj.fillna(result_df, result_cols)
		data = result_df.to_dict('records')
		print (data)
		ret_data = self.validation_obj.duplicate_check_models(request, data, duplicate_comb_check)
		return Response(ret_data)
	
	def nt_account_mapping(self, request, *args, **kwargs):
		"""
		Maps NT accounts after validation.

		Args:
		- request: The HTTP request object.
		- args: Additional arguments.
		- kwargs: Additional keyword arguments.

		Returns:
		- Response: The HTTP response object.
		"""
		self.get_header(request)
		request_data = []
		duplicate_check = True
		if len(kwargs) > 0:
			request_data = kwargs['data']
			self.header.insert(0, 'MappingID')
			duplicate_check = False
		else:
			filename = request.FILES['data_file']
			main_df = pd.read_csv(filename, encoding_errors='ignore')
			request_data = main_df.to_dict('records')
		duplicate_comb_check = ['ClientID', 'NTAccountNumber',
					'NTAccountName', 'PortfolioCode',
					'PrimaryFundCode']
		if duplicate_check:
			request_data = self.validation_obj.duplicate_check_models(request, request_data, duplicate_comb_check)
		if len(request_data) == 0:
			return Response(request_data)
		main_df = pd.DataFrame(request_data, columns=self.header)
		main_df = main_df.dropna(how='all')
		print("\n\nmain_df:\n", main_df)

		main_df = main_df[self.header]
		main_df = self.validation_obj.integer_conversion(main_df, ['ClientID', 'UploadTransactionsDaily', 'UploadValuationsDaily', 'UploadTransactionsMonthly', 'UploadValuationsMonthly'])
		main_df = main_df.fillna('')
		main_df = self.validation_obj.strip_whitespaces(main_df, self.header)
		# check 1: check -> whether client ID is present or not
		
		
		
		main_df = self.validation_obj.check_duplicate_rows(main_df, duplicate_comb_check) 
		# Check for Valid ClientID (clientID provided, but not valid)
		MappingClientIDs = main_df[['ClientID']].drop_duplicates()
		
		ret_dict = self.validation_obj.client_id_empty_check(main_df, self.header)
		main_df = ret_dict['main_df']
		clientid_empty_df = ret_dict['clientid_empty_df']
		main_df = self.validation_obj.client_id_valid_check(main_df)
		# non blank columns -> Source data columns that cannot be left blank
		non_blank_columns = ['Consolidation', 'NTAccountNumber', 'IsSMA',
						'PortfolioCode', 'PrimaryScope', 'PrimaryFundCode', 
						'EntityType', 'SecondaryLegScope']
		main_df['Check -> BlankColumns'] = main_df.apply(
			self.validation_obj.check_blank_column, axis=1, non_blank_columns=non_blank_columns)


		# Check for NSecNum and CSecurityID
		# If IsSMA = 0 and NTAccountName != 'UnitedStatesdollar' 
		# then NSecNum and CSecurityID should not be null. 
		
		main_df['Check -> NSecNum'] = main_df.apply(
			lambda x: 'NSecNum should not be null' if (
				x['IsSMA'] == 0 and x['NTAccountName'] != 'UnitedStatesdollar' and
				(pd.isnull(x['NSecNum']) or x['NSecNum'] == '')) else '', axis=1)

		main_df['Check -> CSecurityId'] = main_df.apply(
			lambda x: 'CSecurityId should not be null' if (
				x['IsSMA'] == 0 and x['NTAccountName'] != 'UnitedStatesdollar' and
				(pd.isnull(x['CSecurityId']) or x['CSecurityId'] == '')) else '', axis=1)


		# Blank value in UploadValuationsDaily, UploadValuationsMonthly,
		# UploadTransactionsDaily, UploadTransactionsDaily
		main_df = self.validation_obj.upload_transactions_and_valuations_check(main_df, ['UploadValuationsDaily', 'UploadValuationsMonthly', 'UploadTransactionsDaily', 'UploadTransactionsMonthly'])

		# SecondaryLegScope and SecondaryLegCode check
		main_df['SecondaryLegScope'] = main_df['SecondaryLegScope'].fillna('')
		main_df['Check -> SecondaryLegScope'] = main_df['SecondaryLegScope'].apply(
			lambda x: 'Please populate a valid secondaryLegScope Value'
			if x and x.lower() not in ['fund', 'cash'] else '')


		# Check Fund Code and Fund ID (changed from mappers insert)
		GetFundsSQL = """\
			SELECT ClientID,FundID as PrimaryUserFundID,FundCode as PrimaryFundCode,FundName as PrimaryFundName ,FundType as PrimaryFundType FROM CaissaMain.dbo.VW_Funds
			"""
		DBFundIDs = ExecuteSQLQuery(GetFundsSQL)

		# Check if line items needs to be tracked(UploadFund)
		main_df["UploadFund"] = main_df[
			["UploadValuationsDaily", "UploadValuationsMonthly",
			"UploadTransactionsDaily"]
		].any(axis=1)

		Mapping_Fund_Code = main_df

		# Drop columns multiple column 
		Mapping_Fund_Code = Mapping_Fund_Code.drop(
			['PrimaryFundName', 'PortfolioName'],
			axis=1)


		Mapping_Fund_Code = Mapping_Fund_Code.merge(
			DBFundIDs, on=['ClientID', 'PrimaryFundCode'], how='left')

		Mapping_Fund_Code['Check -> PrimaryFundCode'] = Mapping_Fund_Code.apply(
			lambda x: 'Please provide correct fund code.' 
			if (pd.isnull(x['PrimaryFundName']) or x['PrimaryFundName']=='') and x['UploadFund'] == True else '', axis=1)


		# Check Portfolio Code
		GetPortfoliosSQL = """\
			SELECT ClientID ,UserPortfolioID as UserPortfolioID,UserPortfolioName as PortfolioName,ClientPortfolioID as PortfolioCode FROM CaissaMain.dbo.UserPortfolio
			"""
		DBPortfoliosIDs = ExecuteSQLQuery(GetPortfoliosSQL)

		Mapping_Fund_Code = Mapping_Fund_Code.merge(
			DBPortfoliosIDs, on=['ClientID', 'PortfolioCode'], how='left')

		Mapping_Fund_Code['Check -> PortfolioCode'] = Mapping_Fund_Code.apply(
			lambda x: 'Invalid PortfolioCode' 
			if (pd.isnull(x['PortfolioName']) or x['PortfolioName']=='') and x['UploadFund'] == True else '', axis=1)


		main_df['Check -> PrimaryFundCode'] = Mapping_Fund_Code['Check -> PrimaryFundCode']
		main_df['Check -> PortfolioCode'] = Mapping_Fund_Code['Check -> PortfolioCode']


		checkcolumns = ['Check -> ClientID',
						'Check -> UploadValuationsDaily',
						'Check -> UploadValuationsMonthly',
						'Check -> UploadTransactionsDaily',
						'Check -> UploadTransactionsMonthly',
						'Check -> BlankColumns',
						'Check -> SecondaryLegScope',
						'Check -> PrimaryFundCode',
						'Check -> PortfolioCode',
		#               'Check -> CommitmentID',
		#               'Check -> ClassID'
						]
		
		cols =['ClientID','UploadValuationsDaily','UploadValuationsMonthly','UploadTransactionsDaily','UploadTransactionsMonthly','BlankColumns','SecondaryLegScope','PrimaryFundCode','PortfolioCode'
						]
		column_to_validate = self.validation_obj.check_column_create(cols)

		main_df['Error'] = main_df.apply(self.validation_obj.error_bool, axis=1,
										checkcolumns=column_to_validate)

		main_df['ErrorMessages'] = main_df.apply(self.validation_obj.error_dict, axis=1,
												checkcolumns=column_to_validate)

		main_df['Error'] = main_df.apply(Validation.error_bool, axis=1,
										checkcolumns=checkcolumns)

		main_df['ErrorMessages'] = main_df.apply(
			Validation.error_dict, axis=1, checkcolumns=checkcolumns)

		
		result_cols = self.header + ['Error', 'ErrorMessages']
		main_df = main_df[result_cols]
		if clientid_empty_df.empty:
			result_df = main_df
		else:
			result_df = pd.DataFrame.from_dict(main_df.to_dict('records') + clientid_empty_df.to_dict('records'))
		main_df = self.validation_obj.revert_to_original(main_df, ['ClientID', 'UploadValuationsDaily', 'UploadValuationsMonthly', 'UploadTransactionsDaily', 'UploadTransactionsMonthly'])
		result_df = self.validation_obj.fillna(result_df, result_cols)
		print("\nfinal result:", result_df.to_dict('records'))
		return Response(result_df.to_dict('records'))


class BatchRecordSearchAPI(APIView):
	"""
	BatchRecordSearchAPI class handles the search of batch records.

	Methods:
	- post: Handles the POST request to search batch records.
	"""

	def post(self, request, *args, **kwargs):
		"""
		Handles the POST request to search batch records.

		Args:
		- request: The HTTP request object.
		- args: Additional arguments.
		- kwargs: Additional keyword arguments.

		Returns:
		- Response: The HTTP response object.
		"""
		params = request.POST.dict()
		feed_id = params.get('FeedID')
		feed_category_id = params.get('FeedCategoryID')
		report_details = get_report_details(request, feed_id, feed_category_id)
		report_details.update(params)
		response_data = report_details
		filter = {'Active': 1}
		if params.get('client_id'):
			filter['ClientID'] = params.get('client_id')
		if report_details['validation_type'] == variable_obj.privateimapping:
			mapping_obj = PrivateiAccMasterMapping.objects.filter(**filter)
			serializers = MappersListSerializer(mapping_obj, many=True)
			data = serializers.data
			mapping_ids = list(mapping_obj.values_list('MappingID', flat=True))
			print (mapping_ids)
			response_data.update({'data':data, 'headers': Headers()._privateiacc_header, 'mapping_ids':json.dumps(mapping_ids)})
		else:
			mapping_obj = NTAccountMapping.objects.filter(**filter)
			serializers = NTAccountListSerializer(mapping_obj, many=True)
			data = serializers.data
			mapping_ids = list(mapping_obj.values_list('MappingID', flat=True))
			print (mapping_ids)
			response_data.update({'data':data, 'headers': Headers()._ntaccounting_header,'mapping_ids':json.dumps(mapping_ids)})
		return Response(data=response_data, status=status.HTTP_200_OK)

class RecordSearchFilterAPI(generics.ListAPIView):
	"""
	RecordSearchFilterAPI class handles the search of records with filters.

	Methods:
	- post: Handles the POST request to search records with filters.
	"""
	
	def post(self, request, *args, **kwargs):
		"""
		Handles the POST request to search records with filters.

		Args:
		- request: The HTTP request object.
		- args: Additional arguments.
		- kwargs: Additional keyword arguments.

		Returns:
		- Response: The HTTP response object.
		"""
		params = request.POST.dict()
		print (params)
		feed_id = params.get('feed_id')
		feed_category_id = params.get('feed_category_id')
		client_id = params.get('client_id')
		report_details = get_report_details(request, int(feed_id), int(feed_category_id))
		filter_dict = json.loads(params.get('filter'))
		kwargs = {
			'{0}__{1}'.format(key, 'contains'): value for key,value in filter_dict.items()}
		kwargs['Active'] = True
		if client_id:
			kwargs['ClientID'] = client_id
		print (kwargs)

		if report_details['validation_type'] == variable_obj.privateimapping:
			mapping_obj = PrivateiAccMasterMapping.objects.filter(**kwargs)
			serializers = MappersListSerializer(mapping_obj, many=True)
			headers =  Headers()._privateiacc_header
		else:
			mapping_obj = NTAccountMapping.objects.filter(**kwargs)
			serializers = NTAccountListSerializer(mapping_obj, many=True)
			headers = Headers()._ntaccounting_header
		mapping_ids = list(mapping_obj.values_list('MappingID', flat=True))
		data = serializers.data
		response_data = {'data':data, 'headers': headers,'mapping_ids':json.dumps(mapping_ids)}
		
		return Response(data=response_data, status=status.HTTP_200_OK)
	
class BatchUpdateAPIview(APIView):
	"""
	BatchUpdateAPIview class handles the update of batch records.

	Methods:
	- post: Handles the POST request to update batch records.
	- delete: Handles the DELETE request to delete batch records.
	"""

	def post(self, request, *args, **kwargs):
		"""
		Handles the POST request to update batch records.

		Args:
		- request: The HTTP request object.
		- args: Additional arguments.
		- kwargs: Additional keyword arguments.

		Returns:
		- Response: The HTTP response object.
		"""
		params = request.POST.dict()
		print (params)
		batch_id = params.get('batch_id')
		action = params.get('action')
		if batch_id:
			batch_obj = Batches.objects.get(BatchID=batch_id)
			if action == 'approve':
				batch_obj.Status = 1
				batch_obj.ApprovedBy = request.user
				batch_obj.ApprovedAt = datetime.today()
			elif action == 'reject':
				batch_obj.Status = 2
				batch_obj.RejectReason = params.get('reason')
				batch_obj.RejectedAt = datetime.today()
				batch_obj.RejectedBy = request.user
			batch_obj.save()
			serializers = BatchListSerializer(batch_obj)
			response = {'data':serializers.data, 'message': 'Batch updated successfully'}
		return Response({'data': response}, status=status.HTTP_200_OK)


	def delete(self, request, *args, **kwargs):
		"""
		Handle the deletion of mapping records.

		This method processes a DELETE request to remove mapping records based on the provided IDs.
		It performs the following steps:
		1. Extracts parameters from the request.
		2. Retrieves the report details based on feed_id and feed_category_id.
		3. If the validation type is 'privateimapping', it updates the 'Active' status of the mappings to 0.
		4. Serializes the updated mapping objects.
		5. Constructs a response with the serialized data, headers, and a success message.

		Args:
			request (HttpRequest): The HTTP request object containing POST data.
			*args: Additional positional arguments.
			**kwargs: Additional keyword arguments.

		Returns:
			Response: A DRF Response object with the serialized data and a success message.
		"""
		params = request.POST.dict()
		mapping_ids = json.loads(params.get('ids'))
		feed_id = params.get('feed_id')
		feed_category_id = params.get('feed_category_id')
		report_details = get_report_details(request, int(feed_id), int(feed_category_id))
		if report_details['validation_type'] == variable_obj.privateimapping:
			headers = Headers()._privateiacc_header
			mapping_obj = PrivateiAccMasterMapping.objects.filter(MappingID__in=mapping_ids)
			mapping_obj.update(**{'Active':0})
			for obj in mapping_obj:
				obj.save()
		serializers = MappersListSerializer(mapping_obj, many=True)
		data = serializers.data
		response = {'data':data, 'headers': headers, 'message': 'Records deleted successfully'}
		response.update(params)
		return Response({'data': response}, status=status.HTTP_200_OK)
		