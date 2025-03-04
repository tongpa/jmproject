# -*- coding: utf-8 -*-
"""Survey Controller"""

from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from pollandsurvey import model
from pollandsurvey.controllers.secure import SecureController
from pollandsurvey.model import DBSession, metadata
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from pollandsurvey.lib.base import BaseController
from pollandsurvey.controllers.error import ErrorController

import sys;
from tg.configuration import AppConfig, config

from tg import tmpl_context
from pollandsurvey.widget.movie_form import create_movie_form
from  logsurvey import LogDBHandler;
__all__ = ['ScriptController']

import logging;
#from model.survey import BasicQuestion
log = logging.getLogger(__name__);

class ScriptController(BaseController):
    
    def __init__(self):
        
        dh = LogDBHandler( config=config,request=request);        
        log.addHandler(dh)
        
    @expose()
    def index(self, came_from=lurl('/')):
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)
    
    #@expose(content_type = 'text/plain; charset=UTF-8')#charset=windows-874')
    @expose(content_type="text/javascript; charset=UTF-8")
    def loadLang(self, lang=None ,**kw):
        reload(sys).setdefaultencoding('utf8')
        language = "en";
        if( lang is not None):
            language = lang;
            
        label = model.LanguageLabel.getAll(1);
        

        str = 'Ext.namespace("survey","survey.label","survey.message");\n';
        
        for l in label:
            str = str + l.module + '.' + l.default_label + '="'  + l.getLang(language)+'";' + '\n';
            #print str;
        
        return str;
    @expose(content_type="text/javascript; charset=UTF-8")
    def loadLangJquery(self, lang=None,**kw):
        reload(sys).setdefaultencoding('utf8');
        
        language = "en";
        if( lang is not None):
            language = lang;
            
        label = model.LanguageLabel.getAll(1);
        

        str = """
        
                {
    "token": {
    "Login": "เข้าสู่ระบบ",
    "Registration" : "ลงทะเบียน",
        "Account": "ข้อมูลผู้ใช้",
        "Property Search":"ค้นหา",
        "Location":"สถานที่ตั้ง",
        "Min Beds":"จำนวนห้องนอน",
        "Property Type":"ชนิดที่อยู่อาศัย",
        "Added In":"ลงประกาศเมื่อ",
        "Show All":"แสดงผลทั้งหมด",
        "House":"บ้าน",
        "Town House":"ทาวน์เฮ้าส์",
        "Apartment":"อพาร์ทเม้นท์",
        "Condominium":"คอนโดมิเนียม",
        "Commercial":"อาคารพาณิชย์",
        "Office":"ออฟฟิศ",
        "Storage":"โกดังเก็บของ",
        "Land":"ที่ดินว่างเปล่า",
        "Anytime":"แสดงผลทั้งหมด",
        "Last 24 Hours":"ชั่วโมงที่ผ่านมา",
        "Last 3 Days":"วันที่ผ่านมา",
        "Last Week":"สัปดาห์ที่ผ่านมา",
        "Last Month":"เดือนที่ผ่านมา",
        "Loading":"กำลังประมวลผล",
        "My Saved Searches":"การค้นหาที่ถูกเก็บไว้",
        "My Listings":"รายการของฉัน",
        "My Analytics":"สถิติผู้เข้าชมประกาศของฉัน",
        "Search Buy":"ซื้อ",
        "Search Rent":"เช่า",
        "Create New Listing":"ลงประกาศ",
        "View My Account":"ดูข้อมูลของฉัน",
        "Property Listing Details":"รายละเอียดประกาศ",
        "Listing Type":"ชนิดของประกาศ",
        "Sell":"ขาย",
        "Let":"เช่า",
        "Lease":"เซ้ง",
        "Floors":"ชั้น",
        "Rooms Total":"จำนวนห้องทั้งหมด",
        "Bedrooms":"ห้องนอน",
        "Bathrooms":"ห้องน้ำ",
        "Kitchens":"ครัว",
        "Property Price and Terms":"ราคาและรูปแบบสัญญา",
        "Price":"ราคา",
        "Term":"สัญญา",
        "Freehold":"มีกรรมสิทธิ์",
        "Leasehold":"มีระยะสัญญา",
        "Possession":"บ้านว่างหรือไม่",
        "Onward Chain":"มีผู้อาศัยอยู่",
        "Vacant Possession":"บ้านว่างพร้อมเข้าอยู่ทันที",
        "Property Location":"สถานที่ตั้ง",
        "Country":"ประเทศ",
        "Post/Zip Code":"รหัสไปรษณีย์",
        "No.":"เลขที่",
        "Road Name":"ชื่อถนน",
        "County/Province":"จังหวัด",
        "Town/City":"อำเภอ",
        "Lease Years Remaining":"จำนวนปีของสัญญาที่เหลือ",
        "day":"วัน",
        "week":"สัปดาห์",
        "month":"เดือน",
        "quarter":"3 เดือน",
        "year":"ปี",
        "Submit Your Listing":"ลงประกาศ",
        "Upload Image":"ใส่รูป",
        "Finish":"เสร็จเรียบร้อย",
        "Search":"ค้นหา",
        "Search...":"ค้นหา",
        "Property Description":"รายละเอียดของประกาศ",
        "Synopsis":"รายละเอียดย่อในประกาศ",
        "Full Description":"รายละเอียดเพิ่มเติมสำหรับผู้สนใจประกาศ",
        "Property Photos":"รูปภาพสถานที่",
          "http://www.ioling.org/images/flags/uk.gif": "http://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_Thailand.svg/1280px-Flag_of_Thailand.svg.png",
        "http://www.google.com/": "http://www.yahoo.com/"
    },
    "regex": [
        ["Budget", "งบประมาณ"],
        ["^Something at start of text", ""],
        ["This will be case insensitive", "i", ""]
    ]
}""";
        
        return str;
    
    
    #@expose(content_type="text/plain")
    @expose(content_type="text/javascript")
    def loadModelObject(self, *args,  **kw):
        
        projectType = model.QuestionProjectType.getAll(1);
        
        modelProjectType = [];
        
        for type in projectType:
            modelProjectType.append(type.to_json());
            
        value = dict(type =modelProjectType );
        import json
        #print json.dumps(value);    
     
        str = """  
            Ext.namespace("survey"); 
            
             
            Ext.define('Survey.model.listQuestionProjectType', {
                extend: 'Ext.data.Model',
                idProperty: 'id_question_project_type',
                fields: ['id_question_project_type', 'description', 'active' ] 
                
            });
            
            survey.listProjectType = new Ext.data.Store({
                model : 'Survey.model.listQuestionProjectType',
                storeId:'listProjectTypeInStore',
                pageSize: 1000,
                data :  """ + json.dumps(value)+ """ ,
                proxy : {
                    type: 'memory',
                    reader: {
                        type: 'json',
                        root: 'type'
                    }
 
                },
                autoLoad : true
            });
        
        """;
        
        variables = model.Variables.getAllParent(1);
        
        modelProjectType = [];
        
        for type in variables:
            modelProjectType.append(type.to_json()); 
        
        value = dict(type =modelProjectType ); 
         
        str = str +  """    
             
            
             
            Ext.define('Survey.model.listVariablesType', {
                extend: 'Ext.data.Model',
                idProperty: 'id_variables',
                fields: ['id_variables', 'name' , 'description', 'id_group_variables', 'table_jm_ref', 'field_jm_ref', 'id_parent', 'childen', 'active'  ] 
                
            });
            
            
            survey.listVariablesType = new Ext.data.Store({
                model : 'Survey.model.listVariablesType',
                storeId:'listVariablesTypeInStore',
                pageSize: 1000,
                data :  """ + json.dumps(value)+ """ ,
                proxy : {
                    type: 'memory',
                    reader: {
                        type: 'json',
                        root: 'type'
                    }
 
                },
                autoLoad : true
            });
        
        """
        
         
        return  str;
            
    
    #@expose(content_type="text/plain")
    @expose(content_type="text/javascript")
    def loadExtjs(self,**kw):
        str = """
        
        (function() {
            function getQueryParam(name) {
                var regex = RegExp('[?&]' + name + '=([^&]*)');
        
                var match = regex.exec(location.search) || regex.exec(path);
                return match && decodeURIComponent(match[1]);
            }
        
            function hasOption(opt, queryString) {
                var s = queryString || location.search;
                var re = new RegExp('(?:^|[&?])' + opt + '(?:[=]([^&]*))?(?:$|[&])', 'i');
                var m = re.exec(s);
        
                return m ? (m[1] === undefined || m[1] === '' ? true : m[1]) : false;
            }
        
            function getCookieValue(name){
                var cookies = document.cookie.split('; '),
                    i = cookies.length,
                    cookie, value;
        
                while(i--) {
                   cookie = cookies[i].split('=');
                   if (cookie[0] === name) {
                       value = cookie[1];
                   }
                }
        
                return value;
            }
        
            var scriptEls = document.getElementsByTagName('script'),
                path = scriptEls[scriptEls.length - 1].src,
                rtl = getQueryParam('rtl'),
                theme = getQueryParam('theme') || 'crisp',
                includeCSS = !hasOption('nocss', path),
                useDebug = hasOption('debug'),
                hasOverrides = !hasOption('nooverrides', path) && !!{
                    // TODO: remove neptune
                    neptune: 1,
                    classic: 1,
                    gray: 1,
                    'neptune-touch': 1,
                    crisp: 1,
                    'crisp-touch': 1
                }[theme],
                repoDevMode = getCookieValue('ExtRepoDevMode'),
                packagePath,
                themePath,
                i = 3,
                overridePath, extPrefix;
        
            rtl = rtl && rtl.toString() === 'true';
        
            while (i--) {
                path = path.substring(0, path.lastIndexOf('/'));
            }
            // path == root of ext
            path = "/javascript/extjs/"    
            theme = 'ext-theme-' + theme;
            packagePath = path + '/packages/' + theme + '/build/';
            themePath = packagePath + 'resources/' + theme + (rtl ? '-all-rtl' : '-all');
             
            if (includeCSS) {
                document.write('<link rel="stylesheet" type="text/css" href="' +
                                    themePath + '-debug.css"/>');
            }
        
            extPrefix = useDebug ? '/ext' : '/ext-all';
            //extPrefix =  '/ext-all-debug'  ;
            
            document.write('<script type="text/javascript" src="' + path + extPrefix +
                                    (rtl ? '-rtl' : '') + '.js"></script>');
        
            if (hasOverrides) {
                // since document.write('<script>') does not block execution in IE, we need to 
                // makes sure we prevent ext-theme-neptune.js from executing before ext-all.js
                // normally this can be done using the defer attribute on the script tag, however
                // this method does not work in IE when in repoDevMode.  It seems the reason for
                // this is because in repoDevMode ext-all.js is simply a script that loads other
                // scripts and so Ext is still undefined when the neptune overrides are executed.
                // To work around this we use the _beforereadyhandler hook to load the neptune
                // overrides dynamically after Ext has been defined.
                overridePath = packagePath + theme + (repoDevMode ? '-debug' : '') + '.js';
        
                if (repoDevMode &&  window.ActiveXObject) {
                    Ext = {
                        _beforereadyhandler: function() {
                            Ext.Loader.loadScript({ url: overridePath });
                        }
                    };
                } else {
                    document.write('<script type="text/javascript" src="' +
                                    overridePath + '" defer></script>');
                }
            }
        
        })();
        
        """;
        
        return str;
    
    
    
    