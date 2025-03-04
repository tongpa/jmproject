# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from tg.decorators import override_template;
from pollandsurvey import model
from pollandsurvey.controllers.secure import SecureController
from pollandsurvey.model import DBSession, metadata
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from pollandsurvey.lib.base import BaseController
from pollandsurvey.controllers.error import ErrorController
from pollandsurvey.widget.register.registerwidget import RegisterForm ,passwordValidator
from pollandsurvey.controllers.utility import Utility
from pollandsurvey.controllers.service import SendMailService,RegisterService,UserObject

from tg import tmpl_context 
from tg.configuration import AppConfig, config
import tw2.core
import logging;
from datetime import datetime ;
log = logging.getLogger(__name__);
from  logsurvey import LogDBHandler;
__all__ = ['RegisterController']


class RegisterController(BaseController):
    """
    The root controller for the PollandSurvey application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    
    def __init__(self):
        self.utility = Utility();  
        self.sendMailService = SendMailService();
        self.registerService = RegisterService();
        
        dh = LogDBHandler( config=config,request=request);        
        log.addHandler(dh)

    def _before(self, *args, **kw):
        tmpl_context.project_name = "pollandsurvey"

    @expose('pollandsurvey.templates.registerform')
    def index(self, *args, **kw):
        """Handle the front-page."""
        return dict(page='index')

    @expose('pollandsurvey.templates.widget')
    def index2(self, *args, **kw):
        w = RegisterForm(redirect='/register/',validate= passwordValidator).req()
        w.child.action ="/register/create";
         
        return dict(widget=w, page='register',title="Register")
    
    @expose('json')
    def create(self,*args,**kw):
        #print kw;
        log.info(kw);
        self.email = kw.get('email');
        self.password = kw.get('password');
        self.rpassword = kw.get('rpassword');
        
        self.success= True;
        self.message = "create success";
        self.urlServer =  model.SystemEnvironment.getServerUrl();
        
        u = model.User.by_email_address(self.email);
        if u is None:
             
            if( str(self.password) ==  str(self.rpassword) ):
                
                 
                self.user,self.userGenCode = self.registerService.createUser(kw);
                
                self.emailValues={};
                self.emailValues['user_name'] = self.user.display_name;
                self.emailValues['email'] = self.user.email_address;
                self.emailValues['password'] = self.password;
                self.emailValues['activate_url'] =  request.scheme   + '://' + self.urlServer + "/activate/" + str(self.userGenCode.code);  #request.application_url
                
                self.sendMailService = SendMailService();
                self.sendMailService.sendActivate(self.emailValues);
                self.sendMailService.start();
                    
                log.info("create user : %s " , self.email);
                
                
            else:
                self.message ="password not same";
                self.success= False;
                log.info("password not same : %s " , self.email);
             
        else:
            self.message = "email have already";
            self.success= False;
            log.info("email have already : %s " , self.email);
        u =None;
        return dict(success=self.success, message = self.message);
    
    @expose('pollandsurvey.templates.register.register_success')
    def registerSuccess(self,*args,**kw):
        
        return dict(page='register_success')
    
    
    @expose( )
    def checkUserEmail(self,*args,**kw):
        #print kw;
        self.email = kw.get('email');
        u = model.User.by_email_address(self.email);
        if u is None:
            return "true";
        return "false";
    
    
    @expose()
    @validate(RegisterForm, error_handler=index)    
    def create_old(self,*args,**kw):
        
        return str(kw);
        flash(_('Wrong credentials'), 'warning')
        email =  kw['registerform:email_address'];
        user = kw['registerform:user_name'];
        confirm_password =  kw['registerform:confirm_password'];
        user_id = kw['registerform:user_id'];
        display = kw['registerform:display_name'];
        password = kw['registerform:password'];
        
        #u = model.User();
        msg ="";
        u = model.User.by_email_address(email);
        if u is None:
            u = model.User.by_user_name(user);
            if u is None:
                log.info("password : " +  password + " , confirm password : " + confirm_password);
                 
                if( str(password) is  str(confirm_password) ):
                    
                    log.info("same password")
                    u= model.User();
                    u.user_name = user
                    u.display_name = display
                    u.email_address = email
                    u.password = password
                    
                    
                    #model.DBSession.add(u)
                    model.DBSession.flush()
                    log.info( "save user success");
                else:
                    msg ="password not same";
                    log.info( "password not same");
            else:
                msg = "user have already";
                log.info( "user have already");
        else:
            msg = "email have already";
            log.info( "email have already");
        
 
    
