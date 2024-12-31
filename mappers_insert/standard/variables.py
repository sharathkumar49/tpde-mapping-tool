
import os
from django.conf import settings 


class Variables:

    def __init__(self):
        self.empty = ""
        self.jsonfilepath = os.path.join(settings.BASE_DIR, "static", "json")
        self.validation_modals = {
            "private_i_acc_mapping": 'PrivateiAccMasterMapping',
            "nt_acc_mapping":  'NTAccountMapping'
        }
        self.privateimapping = 'private_i_acc_mapping' 
        self._common_fields = ['CreatedID', 'UpdatedID', 'CreatedDate', 'UpdatedDate', 'Active', 'MappingID', 'BatchID', 'DuplicateEntry', 'ErrorMessages', 'Error']
       
class Queries:

    def __init__(self):
        self._client_details_query = "SELECT ClientID,ClientName FROM CaissaMain.dbo.Client WHERE IsActive=1"
        self._fund_details_query = "SELECT ClientID ,FundCode as PrimaryFundCode,FundName as PrimaryFundName,FundID as PrimaryUserFundID, FundType as PrimaryFundType, FundCurrency  FROM CaissaMain.dbo.VW_Funds"
        self._portfolio_details_query = "SELECT ClientID ,UserPortfolioID as UserPortfolioID,UserPortfolioName as PortfolioName,ClientPortfolioID as PortfolioCode FROM CaissaMain.dbo.UserPortfolio"
        self._commitments_details_query = "SELECT ClientID,FundCode AS PrimaryFundCode,PortfolioCode,CommitmentCode as CommitmentID,'{}' AS [Check] FROM CaissaMain.dbo.VW_InvestmentsCommitments WHERE ClientID IN {}"
        self.userclass_details_query = "SELECT UserFirm.ClientID,UserFund.ClientFundID as PrimaryFundCode,UserClass.ClientClassID as ClassID,'{}' AS ClassIDCheck FROM CaissaMain.dbo.UserClass JOIN CaissaMain.dbo.UserFund on UserFund.UserFundID = UserClass.UserFundID JOIN CaissaMain.dbo.UserFirm on UserFirm.UserFirmID = UserFund.UserFirmID WHERE UserFirm.ClientID IN {}"

    