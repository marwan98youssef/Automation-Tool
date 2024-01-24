import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
import os

def OAuth():
    #Client Credentials (Bearer token)
    print("\nPlease enter Credentials")
    GENESYS_CLOUD_CLIENT_ID=input("GENESYS_CLOUD_CLIENT_ID:")
    GENESYS_CLOUD_CLIENT_SECRET=input("GENESYS_CLOUD_CLIENT_SECRET:")

    os.environ['GENESYS_CLOUD_CLIENT_ID'] = GENESYS_CLOUD_CLIENT_ID
    os.environ['GENESYS_CLOUD_CLIENT_SECRET'] = GENESYS_CLOUD_CLIENT_SECRET

    try:
        region = PureCloudPlatformClientV2.PureCloudRegionHosts.eu_west_1 #Ireland
        PureCloudPlatformClientV2.configuration.host = region.get_api_host()
        apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(
        os.environ['GENESYS_CLOUD_CLIENT_ID'],
        os.environ['GENESYS_CLOUD_CLIENT_SECRET'])
        print("\nThis Organization is in Ireland (Dublin)")
        
    except:
            try :
                region = PureCloudPlatformClientV2.PureCloudRegionHosts.eu_central_1 #Frankfurt
                PureCloudPlatformClientV2.configuration.host = region.get_api_host()
                apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(
                os.environ['GENESYS_CLOUD_CLIENT_ID'],
                os.environ['GENESYS_CLOUD_CLIENT_SECRET'])
                print("\nThis Organization is in Germany (Frankfurt)")
                
            except ApiException:
                print("\nInvalid Client ID and/or Client Secret")
                exit()
    PureCloudPlatformClientV2.configuration.access_token = apiclient.access_token

def Users():
    Names=input('Enter User Names:')
    NamesList=Names.split(",")
    UsersDict={}
    UsersNotFound=[]
    UsersFound=[]
      # create an instance of the API class
    api_instance = PureCloudPlatformClientV2.UsersApi();
    body = PureCloudPlatformClientV2.UserSearchRequest() # UserSearchRequest | Search request options

    try:
      # Search users
      api_response = api_instance.post_users_search(body)
      for i in range(len(api_response.results)):
            UsersDict.update({api_response.results[i].name: api_response.results[i].id})
    except ApiException as e:
      print("Exception when calling UsersApi->post_users_search: %s\n" % e)
   
    for i in range (len(NamesList)):
            try:
                  UsersFound=UsersFound+[UsersDict[NamesList[i]]]
            except KeyError:
                  UsersNotFound=UsersNotFound+[NamesList[i]]
    if UsersNotFound :
      print('List of Users did not find ID',UsersNotFound )
      print('STOP HERE!!!,please check your input list,then try again')
      exit()
    else:
         return UsersFound

def Queues():
    Names=input("Enter Queues Names:")
    NamesList=(Names.split(","))
    QueuesFound=[]
    QueuesNotFound=[]
    api_instance = PureCloudPlatformClientV2.RoutingApi();
    for i in range (len(NamesList)):

        try:
            # Get list of queues.
            api_response = api_instance.get_routing_queues(name=NamesList[i])
            QueuesFound=QueuesFound+[api_response.entities[0].id]
        except IndexError:
            QueuesNotFound=QueuesNotFound+[NamesList[i]]
    if QueuesNotFound:
        print('List of Queues not find ID',QueuesNotFound)
        print('STOP HERE!!!,please check your input list,then try again')
        exit()
    else:
        return QueuesFound
    
def Wrapupcodes():
    Names=input("Enter Wrapup Codes Names:")
    NamesList=Names.split(",")
    WrapupcodesFound=[]
    WrapupcodesNotFound=[]

    # create an instance of the API class
    api_instance = PureCloudPlatformClientV2.RoutingApi();
    for i in range(len(NamesList)):
        # str | Wrapup code's name ('Sort by' param is ignored unless this field is provided) (optional)
        try:
            # Get list of wrapup codes.
            api_response = api_instance.get_routing_wrapupcodes(name=NamesList[i])
            WrapupcodesFound=WrapupcodesFound+[api_response.entities[0].id]
        except IndexError:
            WrapupcodesNotFound=WrapupcodesNotFound+[NamesList[i]]
    if  WrapupcodesNotFound:
        print('List of Wrapup not find ID', WrapupcodesNotFound)
        print('STOP HERE!!!,please check your input list,then try again')
        exit()
    else:
         return WrapupcodesFound

def Roles():
    Names=input("Enter Roles Names:")
    NamesList=Names.split(",")
    RolesFound=[]
    RolesNotFound=[]

    # create an instance of the API class
    api_instance = PureCloudPlatformClientV2.AuthorizationApi();
    for i in range(len(NamesList)):
         # str |  (optional)
        try:
            # Retrieve a list of all roles defined for the organization
            api_response = api_instance.get_authorization_roles(name=NamesList[i])
            RolesFound= RolesFound+[api_response.entities[0].id]
        except IndexError:
             RolesNotFound=RolesNotFound+[NamesList[i]]
    if  RolesNotFound:
        print('List of Roles not find ID', RolesNotFound)
        print('STOP HERE!!!,please check your input list,then try again')
        exit()
    else:
         return RolesFound

def Users_to_Queues(Users,Queues):
    # create an instance of the API class
    api_instance = PureCloudPlatformClientV2.RoutingApi();
    for i in range(len(Queues)):
        for j in range(len(Users)):
            # str | Queue ID
            # list[WritableEntity] | Queue Members
            #delete bool | True to delete queue members (optional) (default to False)
            try:
             # Bulk add or delete up to 100 queue members
                api_instance.post_routing_queue_members(queue_id=Queues[i] , body=[{"id":Users[j]}], delete=False)
            except ApiException as e:
                print("Exception when calling RoutingApi->post_routing_queue_members: %s\n" % e)
    print("All Users are added successfully to all Queues!!!")

def Wrapupcodes_to_Queues(Wrapupcodes,Queues):
    # create an instance of the API class
    api_instance = PureCloudPlatformClientV2.RoutingApi();
    for i in range(len(Queues)):
        for j in range (len(Wrapupcodes)):
             # str | Queue ID
            # list[WrapUpCodeReference] | List of wrapup codes
            try:
            # Add up to 100 wrap-up codes to a queue
                api_instance.post_routing_queue_wrapupcodes(queue_id=Queues[i], body=[{"id":Wrapupcodes[j]}])
            except ApiException as e:
                print("Exception when calling RoutingApi->post_routing_queue_wrapupcodes: %s\n" % e)
    print("All Wrapup-codes are added successfully to all Queues!!!")
    
def Users_to_Roles(Users,Roles):
    # create an instance of the API class
    api_instance = PureCloudPlatformClientV2.AuthorizationApi();
    for i in range(len(Roles)):
            # str | Role ID
             # list[str] | List of user IDs
            try:
                # Sets the user's roles
                api_instance.put_authorization_role_users_add(role_id=Roles[i], body=Users)
            except ApiException as e:
                print("Exception when calling UsersApi->put_user_roles: %s\n" % e)
    print("All Roles are added to all Users successfully!!!")

def Add_Bulk_Queues():
    Names=input("Enter Queue Names:")
    NamesList=Names.split(",")
    # create an instance of the API class
    api_instance = PureCloudPlatformClientV2.RoutingApi();
    for i in range(len(NamesList)):
    # CreateQueueRequest | Queue
        try:
            # Create a queue
            api_instance.post_routing_queues(body={"name":NamesList[i]})
        except ApiException as e:
            print("Exception when calling RoutingApi->post_routing_queues: %s\n" % e)

def Add_Bulk_Wrapupcodes():
    Names=input("Enter Wrapup Codes Names:")
    NamesList=Names.split(",")
    # create an instance of the API class
    api_instance = PureCloudPlatformClientV2.RoutingApi();
    for i in range(len(NamesList)):
    # WrapupCodeRequest | WrapupCode
        try:
            # Create a wrap-up code
            api_instance.post_routing_wrapupcodes(body={"name":NamesList[i]})
        except ApiException as e:
            print("Exception when calling RoutingApi->post_routing_wrapupcodes: %s\n" % e)

def Add_Bulk_Menu():
    print("\nAdd_Bulk Menu")
    Add_Bulk=input("Press 1: Add Queues\nPress 2: Add Wrapupcodes\n")
    if Add_Bulk=="1":
        Add_Bulk_Queues()
    elif Add_Bulk=="2":
        Add_Bulk_Wrapupcodes()
    else:
        print("You entered:",Add_Bulk,"enter a valid number (1-2)")

def Assignment_Menu():
    print("\nAssignment Menu")
    AssignmentChoices=input("\nPress 1: Assign Users to Queues\nPress 2: Assign Wrapupcodes to Queues\nPress 3: Assign Roles to Users\nPress 4: Go to Add_Bulk Menu\n")
    if AssignmentChoices=="1":
        Users_to_Queues(Users(),Queues())
    elif AssignmentChoices=="2":
        Wrapupcodes_to_Queues(Wrapupcodes(),Queues())
    elif AssignmentChoices=="3":
        Users_to_Roles(Users(),Roles())
    elif AssignmentChoices=="4":
        Add_Bulk_Menu()
    else:
        print("You entered:",AssignmentChoices,"enter a valid number (1-4)")

OAuth()
Assignment_Menu()