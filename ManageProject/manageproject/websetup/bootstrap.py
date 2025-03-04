# -*- coding: utf-8 -*-
"""Setup the manageproject application"""
from __future__ import print_function

import logging
from tg import config
from manageproject import model
import transaction

def bootstrap(command, conf, vars):
    """Place any commands to setup manageproject here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = 'manager'
        u.display_name = 'Example manager'
        u.email_address = 'manager@somedomain.com'
        u.password = 'managepass'
    
        model.DBSession.add(u)
    
        g = model.Group()
        g.group_name = 'managers'
        g.display_name = 'Managers Group'
    
        g.users.append(u)
    
        model.DBSession.add(g)
    
        p = model.Permission()
        p.permission_name = 'manage'
        p.description = 'This permission give an administrative right to the bearer'
        p.groups.append(g)
    
        model.DBSession.add(p)
    
        u1 = model.User()
        u1.user_name = 'editor'
        u1.display_name = 'Example editor'
        u1.email_address = 'editor@somedomain.com'
        u1.password = 'editpass'
    
        model.DBSession.add(u1)
        model.DBSession.flush()
        
        
        task_status = [u'hold',u'start',u'terminate', u'finish',u'revise'];
        for status in task_status:
            ts1 = model.TaskStatus()        
            ts1.description = status;        
            ts1.activate  = '1';
            model.DBSession.add(ts1);
        model.DBSession.flush() 
        
        task_type = [u'requirement',u'design database',u'design gui', u'develop',u'test'];
        
        for type in task_type:
            tts1 = model.TaskType()
            tts1.description = type;
            tts1.activate = '1';
            model.DBSession.add(tts1);
        model.DBSession.flush()
        
        transaction.commit()
    except IntegrityError:
        print('Warning, there was a problem adding your auth data, it may have already been added:')
        import traceback
        print(traceback.format_exc())
        transaction.abort()
        print('Continuing with bootstrapping...')

    # <websetup.bootstrap.after.auth>
