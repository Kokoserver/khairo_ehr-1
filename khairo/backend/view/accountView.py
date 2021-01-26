from fastapi import  APIRouter, status, Depends
from fastapi.background import BackgroundTasks
from fastapi.responses import Response
from mongoengine import errors
from khairo.backend.model.userModel import accountModel
from khairo.backend.model.userModel.accountMixin import AccountManager
from khairo.backend.mixins.generalMixin import KhairoFullMixin
from khairo.backend.model.userModel.accountPydanticModel import (UserRegisterationInput, UserLoginInput,
                                            UserPasswordReset, GetPasswordResetLink)
from khairo.settings import WEBSITE_URL, WEBSITE_NAME, API_BASE_URI

router = APIRouter(prefix=f"{API_BASE_URI}", tags=["User Account"])
@router.post("/register")
def registerUserAccount(user:UserRegisterationInput, background:BackgroundTasks):
    if accountModel.UserAccount.get_singleUserByEmail(email=user.email):
        ErrorResponse = {"message": "Account does not exist"}
        return KhairoFullMixin.Response(userMessage=ErrorResponse, success=False,
                                    status_code=status.HTTP_400_BAD_REQUEST)
    if user.password.strip() == user.confirmPassword.strip():
        try:
            password = AccountManager.hash_password(password=user.password)
            newUserDetails = {
                "firstname": user.firstname,
                "lastname":user.lastname,
                "email": user.email,
                "password": password
            }
            newUser = accountModel.UserAccount(**newUserDetails).save(clean=True)
            if newUser:
                mailData = {
                    "title":"Khairo diet Account verification",
                    "message":f" Welcome to {WEBSITE_NAME}, {newUser.firstname} { newUser.lastname}\n "
                              f"Your account was created successfully please "
                              f"verify your email to continue\n {WEBSITE_URL}{API_BASE_URI}/user/{newUser.id}"
                }
                
                background.add_task(KhairoFullMixin.mailUser, userEmail=newUser.email,
                                             emailTitle=mailData.get("title"),
                                             emailMessage=mailData.get("message"))

                SuccessResponseData = {
                    "user": {"firstname":newUser.firstname, "lastname":newUser.lastname},
                    "message": "Account was created successfully",
                    "confirm email": "A mail was sent to your to confirm your email address"
                    }

                return KhairoFullMixin.Response(userMessage=SuccessResponseData, success=True,
                                                   status_code=status.HTTP_201_CREATED)
            ErrorResponse = {"message": "Error creating account, check your detail and try again"}
            return KhairoFullMixin.Response(userMessage=ErrorResponse, success=False,
                                               status_code=status.HTTP_400_BAD_REQUEST)
        except errors.ValidationError:
            ErrorResponse = {"message": "Error creating account, check your detail and try again"}
            return KhairoFullMixin.Response(userMessage=ErrorResponse, success=False,
                                               status_code=status.HTTP_400_BAD_REQUEST)

        except errors.NotUniqueError:
            ErrorResponse = {"message": "Account with this email already exist, try again"}
            return KhairoFullMixin.Response(userMessage=ErrorResponse, success=False,
                                            status_code=status.HTTP_400_BAD_REQUEST)

    ErrorResponse = {"message": "Password do not match, try again"}
    return KhairoFullMixin.Response(userMessage=ErrorResponse,
                                    success=False,
                                    status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/user/{userId}")
def confirmEmail(userId:str):
    user = accountModel.UserAccount.objects(id=userId).first()
    if user:
        if user.active:
            responseData = {"message": "account already activated", "detail": {
                "login": "you can login in the the url below",
                "url": f"{WEBSITE_URL}/{API_BASE_URI}/login",
                "body": {"email": "string", "password": "string"}
            }}
            return KhairoFullMixin.Response(userMessage=responseData,
                                            success=False,
                                            status_code=status.HTTP_401_UNAUTHORIZED)
        user.update(active=True)
        SuccessResponseData = {
            "user": user.to_json(indent=4),
            "message": "Account verified successfully",
            "extra":{
                "login":"please login to continue",
                "method":"post",
                "body":{"email":"string", "password":"string"}
            }
        }
        return KhairoFullMixin.Response(userMessage=SuccessResponseData,
                                           status_code=status.HTTP_200_OK, success=True)
    ErrorResponseData = {"message": "Account does not exist"}
    return KhairoFullMixin.Response(userMessage=ErrorResponseData,
                                       status_code=status.HTTP_401_UNAUTHORIZED,
                                       success=False)
@router.post("/passwordResetting")
def getPasswordLink(userOldData:GetPasswordResetLink, background:BackgroundTasks):
    user = accountModel.UserAccount.get_singleUserByEmail(email=userOldData.email)
    if user:
            mailData = {
                "title": "Password reset",
                "message": f"password reset pass code\n Password reset link: {WEBSITE_URL}/{API_BASE_URI}/passwordResetting/{user.id}"
            }
            background.add_task(KhairoFullMixin.mailUser, userEmail=user.email,
                                emailTitle=mailData.get("title"),
                                emailMessage=mailData.get("message"))
            ErrorResponseData = {"message": "Check your email for pass code"}
            return KhairoFullMixin.Response(userMessage=ErrorResponseData,
                                               status_code=status.HTTP_200_OK,
                                               success=False)
    ErrorResponseData = {"message": "Account does not exist"}
    return KhairoFullMixin.Response(userMessage=ErrorResponseData,
                                       status_code=status.HTTP_401_UNAUTHORIZED,
                                       success=False)




@router.put("/passwordReset/{userid}")
def passwordReset(userOldData:UserPasswordReset, userId:str):
    user = accountModel.UserAccount.objects(id=userId, email=userOldData.email)
    if user:
            if userOldData.password.strip() == userOldData.confirmPassword.strip():
                newPassword = AccountManager.hash_password(password=userOldData.password)
                if newPassword:
                    user.update(password=newPassword, passwordCode=None)
                    SuccessResponseData = {
                        "user": user.to_json(indent=4),
                        "message": "password change successfully",
                        "extra": {
                            "login": "please login to continue",
                            "method": "post",
                            "body": {"email": "string", "password": "string"}
                        }
                    }
                    return KhairoFullMixin.Response(userMessage=SuccessResponseData,
                                                       status_code=status.HTTP_200_OK, success=True)
                ErrorResponseData = {"message": "could not change password"}
                return KhairoFullMixin.Response(userMessage=ErrorResponseData,
                                                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                   success=False)
            ErrorResponseData = {"message": "password does not match "}
            return KhairoFullMixin.Response(userMessage=ErrorResponseData,
                                               status_code=status.HTTP_400_BAD_REQUEST,
                                               success=False)

    ErrorResponseData = {"message": "Account does not exist"}
    return KhairoFullMixin.Response(userMessage=ErrorResponseData,
                                       status_code=status.HTTP_401_UNAUTHORIZED,
                                       success=False)

@router.post("/login")
def loginUserAccount(userIn:UserLoginInput, response:Response):
    user = accountModel.UserAccount.get_singleUserByEmail(email=userIn.email)
    if user:
        if user.active:
            if AccountManager.check_password(userIn.password, user.password):
                print("password matches")
                encode_jwt_access, encode_jwt_refresh = AccountManager.JwtEncoder(user=user.to_json())
                if encode_jwt_access and encode_jwt_refresh:
                    response.set_cookie(key="refresh_token",
                                        value=encode_jwt_refresh,
                                        httponly=True,
                                        max_age=172800,
                                        expires=172800,
                                        domain=WEBSITE_URL,
                                        secure=True)
                    SuccessResponseData = {
                        "user": user.to_json(indent=4),
                        "message": "logged in successfully",
                        "access_token": encode_jwt_access,
                        "access_token_type": "Bearer",
                        "expires": "2 days"
                    }
                    return KhairoFullMixin.Response(userMessage=SuccessResponseData,
                                                       status_code=status.HTTP_200_OK, success=True)
            ErrorResponseData = {"message": "Password does not match"}
            return KhairoFullMixin.Response(userMessage=ErrorResponseData,
                                               status_code=status.HTTP_401_UNAUTHORIZED,
                                               success=False)

        ErrorResponseData = {"message": "Email was sent to you, please verify your email"}
        return KhairoFullMixin.Response(userMessage=ErrorResponseData,
                                           status_code=status.HTTP_401_UNAUTHORIZED,
                                           success=False)

    ErrorResponseData = {"message": "Account does not exist"}
    return KhairoFullMixin.Response(userMessage=ErrorResponseData,
                                       status_code=status.HTTP_401_UNAUTHORIZED,
                                       success=False)

@router.get("/me")
def getUserAccount(user:dict = Depends(AccountManager.authenticate_user)):
    return user








