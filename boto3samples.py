import boto3
import os
from botocore.exceptions import ClientError

key_ext = '.pem'
key_dir = './'
my_id = 'blthworksproj'
region = 'us-east-1'

ec2 = boto3.client ('ec2', region_name = region)

def create_key_pair(keyname, client):
    """ Creates a key pair with the keyname using boto3.client supplied as client
        Returns True if succesful
        Returns False and error code if fails
    """
    try:
        key = client.create_key_pair(KeyName = my_id)
    except ClientError as e:
        return False, e.response['Error']['Code']
    else:
        return True

def delete_key_pair(keyname, client):
    """ Creates a key pair with the keyname using boto3.client supplied as client
        Returns True if succesful
        Returns True if key is not found
        Returns False and error code if fails
    """
    try:
        res = ec2.delete_key_pair(KeyName = my_id)
    except ClientError as e:
        if e.response['Error']['Code'] == "InvalidKeyPair.NotFound":
            print ("Key not found.")
            return True
        else:
            return False, e.response['Error']['Code']
    else:
        return True

def create_instances(imgId, seckeyname, secgrps, inst_type, placement,
            mincnt, maxcnt, resource, tags = None):
    """ Creates AWS instances with the parameters supplied
        placement is a dict. ex: { 'AvailabilityZone' : 'us-east-1a' }
        The new instances will be tagged if tags parameter is supplied.
        tags parameter is a list of dicts.
    """
    # Start instances
    print ("Launching new instances...")
    try:
        res = resource.create_instances(
                    ImageId = imgId,
                    KeyName = seckeyname,
                    SecurityGroups = secgrps,
                    InstanceType = inst_type,
                    Placement = placement,
                    MinCount = mincnt,
                    MaxCount = maxcnt
                    )
    except ClientError as e:
        return False, e.response['Error']['Code']

    # Create tag for the new instances if parameter supplied
    if tags is not None:
        inst_ids = []
        for instance in res:
            inst_ids.append(instance.id)
        try:
            resource.create_tags(
                Resources = inst_ids,
                Tags = tags
            )
        except ClientError as e:
            return False, e.response['Error']['Code']
        else:
            return True
    else:
        return True
