from django.db import models
from masters.models import GeneralModel, Feeds, FeedCategory
# Create your models here.
from django.contrib.auth.models import User
from datetime import datetime


class ReportTemplates(GeneralModel):
    validation_type = (
        ('private_i_acc_mapping', 'PrivateIAccMapping'),
        ('nt_acc_mapping', "NTAccMapping")
        )
    TemplateID = models.BigAutoField(primary_key=True)
    FeedID = models.ForeignKey(Feeds, on_delete=models.CASCADE)
    FeedCategoryID = models.ForeignKey(FeedCategory, on_delete=models.CASCADE)
    TemplateHeaders = models.TextField(blank=True)
    ReportHeaders = models.TextField(blank=True)
    ValidationType = models.CharField(max_length=255, null=True)

class Batches(GeneralModel):
    status = (
        ('0', 'Waiting For Approval'),
        ('1', 'Approved'),
        ('2', 'Rejected'),
        ('3', 'Completed')
    )
    BatchID = models.BigAutoField(primary_key=True)
    BatchNo = models.CharField(max_length=255, unique=True)
    FeedID = models.ForeignKey(Feeds, on_delete=models.CASCADE)
    FeedCategoryID = models.ForeignKey(FeedCategory, on_delete=models.CASCADE)
    Status = models.CharField(max_length=255, choices=status, default=0)
    ApprovedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)
    RejectedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)
    CompletedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True)
    ApprovedAt = models.DateTimeField(null=True)
    RejectedAt = models.DateTimeField(null=True)
    CompletedAt = models.DateTimeField(null=True)
    RejectReason = models.TextField(null=True)
    RecordCount = models.CharField(max_length=100)
    Configuration = models.ForeignKey(ReportTemplates, on_delete=models.CASCADE)
    UploadType = models.CharField(max_length=255, default='validate-upload')

class PrivateiAccMasterMapping(GeneralModel):
    MappingID = models.BigAutoField(primary_key=True)
    BatchID = models.ForeignKey(Batches, on_delete=models.CASCADE)
    ClientID = models.CharField(max_length=255)
    BurgissPortfolioName = models.CharField(max_length=255)
    UploadValuations = models.CharField(max_length=255)
    PrimaryScope = models.CharField(max_length=255)
    UploadTransactions = models.CharField(max_length=255)
    InvestmentName = models.CharField(max_length=255)
    InvestmentGUID = models.TextField()
    InvestmentID = models.CharField(max_length=255)
    UserPortfolioID = models.CharField(max_length=255)
    PortfolioCode = models.CharField(max_length=255)
    PortfolioName = models.CharField(max_length=255)
    PrimaryUserFundID = models.CharField(max_length=255)
    PrimaryFundName = models.CharField(max_length=255)
    PrimaryFundCode = models.CharField(max_length=255)
    PrimaryFundType = models.CharField(max_length=255)
    EntityType = models.CharField(max_length=255)
    EntryType = models.CharField(max_length=255)
    CommitmentID = models.CharField(max_length=255)
    ClassID = models.CharField(max_length=255)
    TrancheID = models.CharField(max_length=255)
    SecondaryLegCode = models.CharField(max_length=255)
    SecondaryLegScope = models.CharField(max_length=255)
    FundCurrency = models.CharField(max_length=255)
    DuplicateEntry = models.CharField(max_length=255)
    Notes = models.CharField(max_length=255)
    GMTCreatedDate = models.DateTimeField(default=datetime.now())
    GMTModifiedDate = models.DateTimeField(default=datetime.now())
    ErrorMessages = models.JSONField()
    Error = models.BooleanField(default=False)



class NTAccountMapping(GeneralModel):
    MappingID = models.BigAutoField(primary_key=True)
    BatchID = models.ForeignKey(Batches, on_delete=models.CASCADE)
    ClientID = models.CharField(max_length=255)
    Consolidation = models.CharField(max_length=255)
    NTAccountNumber = models.CharField(max_length=255)
    NTAccountName = models.CharField(max_length=255)
    CSecurityId = models.CharField(max_length=255)
    NSecNum = models.CharField(max_length=255)
    IsSMA = models.CharField(max_length=255)
    UploadValuationsDaily = models.CharField(max_length=255)
    UploadTransactionsDaily = models.CharField(max_length=255)
    UploadValuationsMonthly = models.CharField(max_length=255)
    UploadTransactionsMonthly = models.CharField(max_length=255)
    PortfolioCode = models.CharField(max_length=255)
    PortfolioName = models.CharField(max_length=255)
    PrimaryScope = models.CharField(max_length=255)
    PrimaryFundCode = models.CharField(max_length=255)
    PrimaryFundName = models.CharField(max_length=255)
    PrimaryFundType = models.CharField(max_length=255) 
    CommitmentID = models.CharField(max_length=255)
    ClassID = models.CharField(max_length=255)
    TrancheID = models.CharField(max_length=255)
    SecondaryLegScope = models.CharField(max_length=255) 
    SecondaryLegCode = models.CharField(max_length=255) 
    TagDaily = models.CharField(max_length=255)
    TagMonthly = models.CharField(max_length=255) 
    EntityType = models.CharField(max_length=255)
    ErrorMessages = models.JSONField()
    Error = models.BooleanField(default=False)
    DuplicateEntry = models.CharField(max_length=255)


