# -*- coding: utf-8 -*-
"""Survey Controller"""

from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context,validate,response 
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg.configuration import AppConfig, config
from tg import predicates
from pollandsurvey import model
from pollandsurvey.controllers.secure import SecureController
from pollandsurvey.model import DBSession, metadata
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from pollandsurvey.lib.base import BaseController
from pollandsurvey.controllers.error import ErrorController
from pollandsurvey.controllers.utility import Utility
from pollandsurvey.controllers.service import SendSurveyService,SendMailService;

import sys
import json 
import types
from datetime import datetime
from tg import tmpl_context
from pollandsurvey.widget.movie_form import create_movie_form
from pollandsurvey.util import URLUtility
import logging;
log = logging.getLogger(__name__);
from logsurvey import LogDBHandler
__all__ = ['SurveyController']


class SurveyController(BaseController):
    
    def __init__(self):
        self.utility = Utility();
        self.urlUtility = URLUtility();
        self.UPLOAD_DIR = config['path_upload_file'] ;
        
        dh = LogDBHandler( config=config,request=request);
        
        log.addHandler(dh)
    
    def _before(self, *args, **kw):
        tmpl_context.project_name = "pollandsurvey"
    
    
    @expose('pollandsurvey.templates.surveyjs.index')
    #@expose('pollandsurvey.templates.listsurvey.index')
    @require(predicates.not_anonymous(  msg=l_('Only for Authen')))
    def listsetup(self, came_from=lurl('/'), *args, **kw):
        """Handle the front-page."""
        reload(sys).setdefaultencoding("utf-8");
        
        
        #groups = request.identity['groups'] ;
        
        return dict(page='survey')
    
    
    @expose('json')
    def getProject(self, *args, **kw):
        
        self.page = kw.get('page');
        self.pagesize = kw.get('pagesize');
        
        print ( "page : %s " %self.page);
        print ( "page size : %s " %self.pagesize);
        
        user =  request.identity['user']; 
        
        quest_project = [];
         
        quest_project.append({'survey_name': "test1", 'duration_date' :   '2015/10/01', 'survey_type' : 'exam', 'status' : 'Finish','url'  : 'localhost' })
        quest_project.append({'survey_name': "test2", 'duration_date' :   '2015/10/01', 'survey_type' : 'exam', 'status' : 'Finish','url'  : 'localhost' })
        #quest_project.append({'survey_name': "test3", 'duration_date' :   '2015/10/01', 'survey_type' : 'exam', 'status' : 'Finish','url'  : 'localhost' })
        #quest_project.append({'survey_name': "test4", 'duration_date' :   '2015/10/01', 'survey_type' : 'exam', 'status' : 'Finish','url'  : 'localhost' })
        #quest_project.append({'survey_name': "test5", 'duration_date' :   '2015/10/01', 'survey_type' : 'exam', 'status' : 'Finish','url'  : 'localhost' })
        #quest_project.append({'survey_name': "test5", 'duration_date' :   '2015/10/01', 'survey_type' : 'exam', 'status' : 'Finish','url'  : 'localhost' })
        
        
        
        return dict(historys = quest_project,length = 6);
    
    
    @expose('pollandsurvey.templates.survey.samplegrid')
    @require(predicates.in_any_group('voter','managers', msg=l_('Only for voter')))
    def samplegrid(self, *args, **kw):
        """Handle the front-page."""
        reload(sys).setdefaultencoding("utf-8");
        return dict(page='index')
    
    @expose('pollandsurvey.templates.survey.index_new')
    def sampleMVC(self,*args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        log.info("survey controller index");
        
        return dict(page='index')
     
    @expose('json')
    def readstudent(self,*args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        log.info("survey controller index");
        
        self.message = "message from server";
        self.success = True;
        self.data = [];
        
        self.data.append({"Id":1,"address1":"","address2":"","birthDate":None,"city":"","firstName":"","lastName":"","middleName":"","state":""});
        
        
        return dict(message = self.message, success = self.success, data =self.data)
    
    
     
     
        
    @expose('pollandsurvey.templates.survey.index')
    @require(predicates.in_any_group('creator','managers', msg=l_('Only for creator')))
    def index(self, *args, **kw):
        """Handle the front-page."""
        reload(sys).setdefaultencoding("utf-8");
        
        log.info("survey controller index");
        
        return dict(page='index')
    
    @expose('json')
    @require(predicates.not_anonymous(  msg=l_('Only for Authen')))
    def getProjectByUser(self, came_from=lurl('/'),*args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        
        user =  request.identity['user']; 
        
        quest_project = model.QuestionProject.getAllByUser(1,user.user_id);
        
        log.info("getProjectByUser");
        return dict(survey=quest_project , total = len(quest_project));
    
    @expose('json')
    def getAll(self, *args, **kw):
        question = model.QuestionType.getAll(1);
        return dict(page ="test",quest = question) ;
    
    
    @expose('pollandsurvey.templates.survey.index')
    def extjs(self, *args, **kw):
        """Handle the front-page."""
        return dict(page='index')
    
    
    @expose('json')
    def updateProject(self, came_from=lurl('/'), *args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        self.success = True;
        self.message = "success";
        
        id_question_project = kw.get('id_question_project');
        description = kw.get('description');
        end_text = kw.get('end_text');
        footer_message = kw.get('footer_message');
        header_message = kw.get('header_message');
        id_question_project_type = kw.get('id_question_project_type');
        name = kw.get('name'); 
        welcome_text = kw.get('welcome_text'); 
        
        if id_question_project is not None or id_question_project != '':
            project = model.QuestionProject.getId(id_question_project);
            if(project):
                project.description = description;
                project.end_text = end_text;
                project.footer_message = footer_message;
                project.header_message = header_message;
                project.name = name;
                project.welcome_text = welcome_text;
                project.id_question_project_type = id_question_project_type;
                
            else :
                self.message = "error";
        else:
            self.message = "error";
        
        return dict(success=self.success, message = self.message);
        
    @expose('json')
    def deleteProject(self, came_from=lurl('/'), *args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        self.success = True;
        self.message = "success";
        
        self.df = json.loads(request.body, encoding=request.charset);
        
         
        self.idProject = self.df.get('id_question_project');
        
        self.listQuestion = model.Question.getByProjectId(self.idProject);
        for self.question in self.listQuestion:
            if(self.question):
                self.idQuestion = self.question.id_question;
                model.Question.deleteQuestoin(self.idQuestion);
            
        model.QuestionProject.deleteById(self.idProject);
        
        return dict(success=self.success, message = self.message);
    
    @expose('json')
    def saveitems(self, came_from=lurl('/'), *args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        self.success = True;
        self.message = "success";
        
        return dict(success=self.success, message = self.message);
    
    @expose('json')
    @require(predicates.not_anonymous(  msg=l_('Only for Authen')))
    def saveProject(self, came_from=lurl('/'), *args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        self.success = True;
        self.message = "success";
         
        
        project = model.QuestionProject();
        
        user =  request.identity['user']; 
        project.user_id =  user.user_id;
        
        log.info(kw );
        
        
        if 'description' in kw:
            project.description = kw.get('description');
        
        if 'id_question_project_type' in kw:
            project.id_question_project_type = kw.get('id_question_project_type');
            
        if 'name' in kw:
            project.name = kw.get('name');
       
       
       
       
        if 'id_question_project' in kw  :
            #project.id_question_project =  kw.get('id_question_project');
            
            project.save();
        
        
        
        return dict(success=self.success, message = self.message);
        #return dict(failed=self.success, message = self.message);
        
   
    
    @expose('json')
    def deleteQuestion(self, came_from=lurl('/'), *args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        
        self.success = True;
        self.message = "Save Success";
        
        df = json.loads(request.body, encoding=request.charset);
        
        log.info(df);
        log.info(df.get('id_question') );
        
        #question = model.Question.loadJson(df);
        
        #question = model.Question.getById(df.get('id_question'));
        
        idQuestion = df.get('id_question');
        
        self.success, self.message = model.Question.deleteQuestoin(idQuestion);

        
        return dict(success=self.success, message = self.message);
   
    
    
    
    
        
    @expose('json',content_type="text/plain" )
    @require(predicates.not_anonymous(  msg=l_('Only for Authen')))
    def addQuestion(self, came_from=lurl('/'), *args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        self.success = True;
        self.message = "success";
        self.result = True;
        log.info("add Question");
        self.dataValue = kw;
        log.info(kw);
        log.info('----------');
        log.info(args);
        log.info('----------');
        
    
        
        
        
        user =  request.identity['user']; 
        
        #model.Question.createQuestion(self.dataValue,user.user_id);
        log.info("check");
        
        self.isCreate = self.dataValue.get('id_question') is None or ( len(self.dataValue.get('id_question')) == 0 );
        
        self.id_question_type  = self.dataValue.get('id_question_type')
        #create or update question
        question = model.Question();
        if( self.isCreate  ):
            log.info("---------- create question---------------------");
            question.question = self.dataValue.get('question');
            question.help_message = self.dataValue.get('help_message');
            question.id_question_project = self.dataValue.get('id_question_project');
            question.id_question_type = self.id_question_type;
            
            question.text_label = '';
            question.user_id = user.user_id;
            question.order = self.dataValue.get('order');  
            question.score = self.dataValue.get('score');  
            question.id_fix_difficulty_level = self.dataValue.get('id_fix_difficulty_level');
            
            question.save();
            
            log.info(question.id_question);
        else:
            log.info("---------- update question---------------------");
            question = model.Question.getById(self.dataValue.get('id_question'));
            if(question):
                question.help_message = self.dataValue.get('help_message');
                question.text_label = '';
                question.question = self.dataValue.get('question');
                question.score = self.dataValue.get('score');  
                
                question.id_fix_difficulty_level = self.dataValue.get('id_fix_difficulty_level');
                 
                question.user_id = user.user_id;
            else:
                log.info("error question is not found");
                self.success = True;
                self.message = "question is not found";
                return dict(success=self.success, message = self.message); 
                
        log.info("save Question");
            
        # create or update questionMedia    
        imageFile = self.dataValue.get('image_upload');
        if type(imageFile) is types.InstanceType:
            
            self.file_name = imageFile.filename;
            self.file_data = imageFile.value;
            self.target_file_name = self.utility.joinPathFileAndCreatePath(self.UPLOAD_DIR, str(question.id_question), self.file_name);
              
            self.utility.saveFile(self.target_file_name,self.file_data);  
            
            questionMedia = model.QuestionMedia.getId(question.id_question);
            if(questionMedia is None):
                questionMedia = model.QuestionMedia();
                questionMedia.id_question = question.id_question;
            else:
                self.utility.removeFile(questionMedia.media_path_file);
                log.info('remove file : ' + questionMedia.media_path_file );
            questionMedia.value = self.file_name;
            questionMedia.media_type = imageFile.type;
            questionMedia.media_path_file = self.target_file_name;
            questionMedia.save();
            
            log.info("save questionMedia"); 
            
        #Step 2 create         
        datagrid  = json.loads(self.dataValue.get('datagrid'));
        for basic_datas in datagrid:  
            log.info(basic_datas);
            self.isCreate = basic_datas.get('id_question') is not None and len( str(basic_datas.get('id_question')).strip() ) > 0 ;
            
            basicData = model.BasicData();
            basicQuestion = model.BasicQuestion();
            log.info("-----------------------Basic data-----------------------------------");
            if (not self.isCreate ):
                log.info ("create basic data");                
                basicData.id_basic_data_type = self.id_question_type; #image
                basicData.save();  
                
                log.info ("create basic question");
                basicQuestion.id_question = question.id_question;
                basicQuestion.id_basic_data = basicData.id_basic_data;
                basicQuestion.answer =   basic_datas.get('answer') ;# ({True: True, False: False}[ basic_datas.get('answer') in 'true']);
                basicQuestion.score =   basic_datas.get('score') ;
                basicQuestion.order = basic_datas.get('seq');                    
                basicQuestion.save();              
            else:
                log.info ("update basic data : " + str( basic_datas.get('id_basic_data')) );                
                basicData.id_basic_data = basic_datas.get('id_basic_data');
                basicQuestion  = model.BasicQuestion.getByQuestionAndBasic(question.id_question, basicData.id_basic_data);
                if(basicQuestion):
                    basicQuestion.answer =   basic_datas.get('answer') ; 
                    basicQuestion.score =   basic_datas.get('score') ;
                    basicQuestion.order = basic_datas.get('seq');    
                else:
                    log.info("error load basicQuestion");
           
            log.info("------------------------basic Data type----------------------------------" );
            log.info('self.id_question_type : ' + str(self.id_question_type)  + ' type : ' + type(self.id_question_type).__name__ ) ;
            if ( self.id_question_type in ['1','2','3','4','5','6','7'] ):
                log.info("case text");
                basicText = model.BasicTextData();
                if (not self.isCreate ):
                    log.info("create basic text");
                    basicText.id_basic_data = basicData.id_basic_data;
                    basicText.value = basic_datas.get('value');
                    basicText.save();
                else:
                    log.info("update basic text");
                    basicText = model.BasicTextData.getByBasicDataId(basicData.id_basic_data);
                    if(basicText):                
                        basicText.value = basic_datas.get('value');                       
                    else:
                        log.info("error load BasicTextData");    
                
            elif (self.id_question_type == '4'):
                log.info("case image");
                answerimage = self.dataValue.get('answer_image');
                log.info(basic_datas.get('answer_image'));
                log.info(type(answerimage));
                
                log.info('basicData.id_basic_data : ' + str(basicData.id_basic_data));
                
                if (type(answerimage) is types.InstanceType or  type(answerimage) is types.ListType) :
                    if  type(answerimage) is types.InstanceType:
                        log.info('single file');
                        log.info(answerimage.type);
                        file = answerimage;
                        if( self.utility.isPartOf(file.filename,basic_datas.get('answer_image')) ):
                        #if (basic_datas.get('answer_image') == file.filename ) :
                            basicMedia = model.BasicMultimediaData();
                            self.file_name = file.filename;
                            self.file_data = file.value;
                            self.media_type = file.type;
                            self.target_file_name= self.utility.joinPathFileAndCreatePath(self.UPLOAD_DIR, str(question.id_question), self.file_name);
                            self.utility.saveFile(self.target_file_name,self.file_data); 
                            
                            if ( not self.utility.isNumber( basic_datas.get('id_basic_data') ) ):
                                log.info('create basic media');
                                basicMedia.id_basic_data = basicData.id_basic_data;
                                basicMedia.value = self.file_name;
                                basicMedia.media_type = self.media_type;
                                basicMedia.media_path_file = self.target_file_name;
                                basicMedia.save();
                            else:
                                log.info('update basic media');
                                basicMedia = model.BasicMultimediaData.getByBasicDataId(basic_datas.get('id_basic_data') );
                                self.utility.removeFile(basicMedia.media_path_file);
                                basicMedia.value = self.file_name;
                                basicMedia.media_type = self.media_type;
                                basicMedia.media_path_file = self.target_file_name;
                                
                    else:
                        for file in answerimage:
                            log.info('type list file');
                            log.info(type(file));
                            if type(file) is not types.UnicodeType:
                                
                                #print file.type;
                                if( self.utility.isPartOf(file.filename,basic_datas.get('answer_image')) ):
                                #if (basic_datas.get('answer_image') == file.filename) :
                                    self.file_name = file.filename;
                                    self.file_data = file.value;
                                    self.media_type = file.type;
                                    self.target_file_name= self.utility.joinPathFileAndCreatePath(self.UPLOAD_DIR, str(question.id_question), self.file_name);
                                    self.utility.saveFile(self.target_file_name,self.file_data); 
                                    basicMedia = model.BasicMultimediaData();
                                    if ( not self.utility.isNumber( basic_datas.get('id_basic_data') ) ):
                                        log.info('create basic media');
                                        basicMedia.id_basic_data = basicData.id_basic_data;
                                        basicMedia.value = self.file_name;
                                        basicMedia.media_type = self.media_type;
                                        basicMedia.media_path_file = self.target_file_name;
                                        basicMedia.save();
                                    else:
                                        log.info('update basic media');
                                        basicMedia = model.BasicMultimediaData.getByBasicDataId(basic_datas.get('id_basic_data') );
                                        self.utility.removeFile(basicMedia.media_path_file);
                                        basicMedia.value = self.file_name;
                                        basicMedia.media_type = self.media_type;
                                        basicMedia.media_path_file = self.target_file_name;
                  
                else:
                    log.info("Other type");
                    
                pass;
             
            
        log.info("save object");
        
        
        
        return dict(success=self.success, message = self.message, result = self.result);
    
    
    @expose('json')
    def createBasicData(self, came_from=lurl('/'), *args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        
        
        self.success = True;
        self.message = "success";
        log.info(request);
        log.info(args);
        log.info(kw);
        
        return dict(success=self.success, message = self.message);
    
    @expose('json')
    def updateQuestionData(self, **kw):
        reload(sys).setdefaultencoding("utf-8");
       
        self.success = True;
        self.message = "success";
        log.info('---------1--------------');
        #log.info(request.method );
        #log.info(request.params );
        
        df = json.loads(request.body, encoding=request.charset);
        for d in df:
            log.info(d.get('id_question'));
            log.info(d.get('order'));
            self.success, self.message = model.Question.updateOrderById(d.get('order'), d.get('id_question'));
            
            log.info(self.success);
            log.info(self.message);
            
        #for d in request:
        #    log.info(d);
        log.info(df);
        log.info('-----------------------');
        log.info(kw);
       
        return dict(success=self.success, message = self.message);
    
    @expose('json')
    def deleteMediaQuestion(self, came_from=lurl('/'), *args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        self.success = True;
        self.message = "success";
        log.info('---------1--------------');
        
        df = json.loads(request.body, encoding=request.charset);
        
        model.QuestionMedia.deleteByQuestion(df.get('id'));
        
        return dict(success=self.success, message = self.message);
    
    @expose('json')
    def deleteQuestionData(self, came_from=lurl('/'), *args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        self.success = True;
        self.message = "success";
        log.info('---------1--------------');
        
        df = json.loads(request.body, encoding=request.charset);
        # remark : remove file
        self.success,self.message =  model.BasicQuestion.deleteData(df.get('id'), deleteBasicQuestion=True) ;
        
        return dict(success=self.success, message = self.message);
    
    
    @expose('json')
    def addOptions(self, came_from=lurl('/'), *args, **kw):
        reload(sys).setdefaultencoding("utf-8");
        self.success = True;
        self.message = "success";
        self.result = True;
        log.info('---------1--------------');
         
     
        log.info(kw);
        log.info(args);
        
        
        self.option = model.QuestionOption();   
         
        if(not self.utility.isEmpty(kw.get('id_question_option'))):
            self.option = model.QuestionOption.getId(kw.get('id_question_option')  ); 
            
            
             
        self.option.id_question_project = kw.get('id_question_project');        
        self.option.id_question_theme = kw.get('id_question_theme'); 
        self.option.name_publication = kw.get('name_publication');
        self.option.id_close_type = kw.get('id_close_type');
        
        self.option.id_fix_random_type = kw.get('id_fix_random_type');
        
        if (not self.utility.isEmpty(kw.get('activate_date'))):
            self.option.activate_date =  datetime.strptime(kw.get('activate_date')  + ' 00:00:00' , '%d/%m/%Y %H:%M:%S') ;
        
        if (not self.utility.isEmpty(kw.get('expire_date'))):
            self.option.expire_date =  datetime.strptime(kw.get('expire_date')  + ' 23:59:59' , '%d/%m/%Y %H:%M:%S') ;
       
        
        self.option.id_question_invitation = kw.get("id_question_invitation");
        self.option.header_message =kw.get('header_message');
        self.option.footer_message = kw.get('footer_message');
        self.option.welcome_message = kw.get('welcome_message');
        self.option.end_message = kw.get('end_message');
        self.option.use_question_no = kw.get('use_question_no');
        self.option.duration_time   = kw.get('duration_time');
        self.option.random_answer = int ( kw.get('random_answer') ); 
        self.option.show_score = self.utility.convertToBit(kw.get('show_score')) ;    
        
        self.option.show_navigator = self.utility.convertToBit(kw.get('show_navigator')) ;         
        self.option.redirect_url =kw.get('redirect_url');
        
        if (  self.utility.isEmpty(kw.get('id_question_option'))):
            log.info("save option");
            self.option.save();
       
            
       
        
        
        
        
        
        return dict(success=self.success, message = self.message,result = self.result);
    
    
    @expose('json')
    def deleteOptions(self, came_from=lurl('/'), *args, **kw):
         
        reload(sys).setdefaultencoding('utf8')
        
        
        self.success = True;
        self.message = "Save Success";
        
        df = json.loads(request.body, encoding=request.charset);
        
        log.info(df);
        log.info(df.get('id_question_option'));
        
         
        idQuestion = df.get('id_question_option');
        
        self.success, self.message = model.QuestionOption.deleteById(idQuestion);

        
        return dict(success=self.success, message =self.message);
    
    
    @expose('json')
    def addInvitation(self, **kw):
        reload(sys).setdefaultencoding('utf8')
        
        log.info( kw);
        log.info( kw.get('id_question_invitation'));
        #print kw.get('content');
        log.info( str(kw.get('subject')).encode('utf-8'));
        log.info( kw.get('id_question_project'));
        log.info( str(kw.get('from_name')).encode('utf-8'));
        
        
        self.success = True;
        self.message = "Save Success";
        self.result = True;
        try:
            
            self.template = model.Invitation();
            
            if ( not self.utility.isEmpty(kw.get('id_question_invitation'))):
                self.template = model.Invitation.getId(kw.get('id_question_invitation')); 
                
            
            
            self.template.name_content = kw.get('name_content');
            self.template.from_name = kw.get('from_name');
            self.template.subject = kw.get('subject');
            self.template.id_question_project = kw.get('id_question_project');
            self.template.content = kw.get('content');
            
            if (  self.utility.isEmpty(kw.get('id_question_option'))):
                log.info("save email template");
                self.template.save();
        except Exception as e:
            self.result = False;
            self.message = '' + str(e);
            
        log.info( self.message);        
        
        return dict(success=self.success, message = self.message, result= self.result);
    
    
    @expose('json')
    def addVoterToInvitation(self,**kw):
        reload(sys).setdefaultencoding('utf8')
        
        log.info( kw);
        
        self.success = True;
        self.message = "Save Success";
        return dict(success=self.success, message = self.message);
    
    
    @expose('json')
    @require(predicates.in_any_group('voter', 'managers', msg=l_('Only for voter')))
    def deleteInvitation(self, **kw):
        reload(sys).setdefaultencoding('utf8')
        self.success = True;
        self.result = True;
        self.message = 'Delete Success';
        try:
            df = json.loads(request.body, encoding=request.charset);
            
            log.info(df);
            log.info(df.get('id_question_invitation'));
            
            
            
            self.result =model.Invitation.deleteById(df.get('id_question_invitation'));
            
            if not self.result:
                self.message = 'Can not Delete.'; 
            
            
        except Exception as e:
            self.result =False;
            self.message = '' + str(e);
            
        
        return dict(success=self.success, result =self.result, message =self.message);
    
    
    @expose('json')
    @require(predicates.in_any_group('voter', 'managers', msg=l_('Only for voter')))
    def sendSurvey(self, **kw):
        reload(sys).setdefaultencoding('utf8')
        self.success = True;
        self.result = True;
        self.message = 'Send Success';
        
        
        try:
            df = json.loads(request.body, encoding=request.charset);
            
            log.info(df);
            log.info(df.get('id_question_option'));
            log.info(df.get('id_question_project'));
            log.info(df.get('id_question_invitation'));
            
            self.option = model.QuestionOption.getId(df.get('id_question_option'));
            
            if self.option.send_status == 0:
                
                self.emailtemplate = model.Invitation.getId(df.get('id_question_invitation'));
                if(self.emailtemplate is not None):
                    
                    #self.sendSurveyService = SendSurveyService();
                    #self.sendSurveyService.setEmailToVoter(model,self.option,self.emailtemplate);
                    #self.sendSurveyService.start();
                    
                    user =  request.identity['user'];
                    
                    self.voters, self.leng =model.Voter.getVoter(user.user_id, page=0, page_size=100); 
                    
                    self.urlServer =  model.SystemEnvironment.getServerUrl();
        
                    for v in self.voters:
                        #print v;
                        self.resp = model.Respondents.getByVoterIdAndPublicId(v.id_voter,self.option.id_question_option);
                        if (self.resp is None):
                            self.resp = model.Respondents();
                            self.resp.id_voter = v.id_voter;
                            self.resp.id_question_project = self.option.id_question_project;
                            self.resp.id_question_option =self.option.id_question_option;
                            self.resp.key_gen = self.utility.my_random_string(string_length=25)
                            self.resp.save();
                        
                        if (self.resp.key_gen is None):
                            self.resp.key_gen = self.utility.my_random_string(string_length=25)
                        
                        
                        self.emailValues={};
                        self.emailValues['name'] = str(v.firstname) + " " + str(v.lastname);
                        self.emailValues['email'] = v.email;
                        self.emailValues['subject'] = self.emailtemplate.subject;
                        self.emailValues['from'] =  self.emailtemplate.from_name;
                        #self.emailValues['url'] = self.urlUtility.URL_REPLY.format(self.urlServer, str(self.option.id_question_project), str(self.option.id_question_option), str(v.id_voter))  ; #request.application_url
                        self.emailValues['url'] = self.urlUtility.URL_QUESTIONNAIRE.format(nameserver=self.urlServer,key=self.resp.key_gen);  #self.urlUtility.URL_REPLY.format(self.urlServer, str(self.option.id_question_project), str(self.option.id_question_option), str(v.id_voter))  ; #request.application_url
                        self.emailValues['initialDate'] = str(self.option.activate_date);
                        self.emailValues['finishDate'] = str(self.option.expire_date);
                        
                         
                        
                        template = self.emailtemplate.content;
                        for k, va in  self.emailValues.iteritems():
                            template = template.replace('[%s]' % k, va)
                            
                        self.sendmail = model.SendMail(id_question_option = self.resp.id_question_option,
                                                       id_voter = self.resp.id_voter, 
                                                       user_id =None,
                                                       sender_name = self.emailtemplate.from_name,
                                                       receive =  v.email,
                                                       subject = self.emailtemplate.subject,
                                                       content = template);
                                                       
                        self.sendmail.save();
                        
                        
                        sendmail  = SendMailService();
                        sendmail.sentEmail(self.emailValues, template);
                        
                        self.sendmail.sended_date = datetime.now();
                        self.sendmail.status = 'F';
                       
                        
                    
                else:
                    self.result = False;
                    self.message = "Please select template email.";
                
                
                #self.result,self.message =  model.QuestionOption.updateSendStatus(1,df.get('id_question_option'));
                
                log.info( "\n send to thread");
            else:
                self.result = False;
                self.message = "system found send already"; 
            
            #model.Invitation.deleteById(df.get('id_question_invitation'));
             
            
        except Exception as e:
            log.error(e);
            self.result = False;
            self.message = '' + str(e);
            
        
        return dict(success=self.success, result=self.result, message=self.message);
    
     
        
        
        
        
    