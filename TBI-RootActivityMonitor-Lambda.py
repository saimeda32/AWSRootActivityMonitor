# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
# Description: This Lambda function sends an SNS notification to a given AWS SNS topic when an API call event by IAM root user is detected.
#              The SNS subject is- "API call-<insert call event> by Root user detected in Account-<insert account alias>, see message for further details". 
#              The JSON message body of the SNS notification contains the full event details.
# 
#
# Author: Sudhanshu Malhotra


import json
import boto3
import logging
import os
import botocore.session
from botocore.exceptions import ClientError
session = botocore.session.get_session()

logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger(__name__)

def lambda_handler(event, context):
	logger.setLevel(logging.DEBUG)
	eventname = event['detail']['eventName']
	snsARN = os.environ['SNSARN']          #Getting the SNS Topic ARN passed in by the environment variables.
	user = event['detail']['userIdentity']['type']
	account = event['account']
	
	logger.debug("Event is --- %s" %event)
	logger.debug("Event Name is--- %s" %eventname)
	logger.debug("SNSARN is-- %s" %snsARN)
	logger.debug("User Name is -- %s" %user)
	
	client = boto3.client('iam')
	snsclient = boto3.client('sns')
	
	
	#### Below needs to be tested ##SAI MEDA
	
#	response = client.list_account_aliases()
#	logger.debug("List Account Alias response --- %s" %response)
	
#'''	try:
#		if not response['AccountAliases']:
#			accntAliase = (boto3.client('sts').get_caller_identity()['Account'])
#			logger.info("Account Aliase is not defined. Account ID is %s" %accntAliase)
#		else:
#			accntAliase = response['AccountAliases'][0]
#			logger.info("Account Aliase is : %s" %accntAliase) 
#	
#	except ClientError as e:
#		logger.error("Clien Error occured") '''
	
	try: 
		#Sending the notification...
		snspublish = snsclient.publish(
						TargetArn= snsARN,
						Subject=(("Root API call \"%s\" detected in Account: \"%s\"" %(eventname,account))[:100]),
						Message=json.dumps({'default':json.dumps(event)}),
						MessageStructure='json')
		logger.debug("SNS publish response is-- %s" %snspublish)
	except ClientError as e:
		logger.error("An error occured: %s" %e)