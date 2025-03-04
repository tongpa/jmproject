
 


Ext.define('survey.panel.ManageVoters',{
	//extend : 'Ext.panel.Panel', 	 
	extend : 'Ext.form.Panel',
	alias: ['widget.manageVoters'],
	layout: 'fit',
	defaults: {
        anchor: '100%',
        labelWidth: 120
    },
	frame: true,
	
	height : 500,
	bodyPadding: 10,
	showClose : true,
    
    isCreate : true,
    parentForm : null,
    initComponent: function() {
		
		var main = this;
		
		
		
		
		main.store.load();
		main.selectVoters = Ext.create(
				//'Ext.ux.form.ItemSelector' 
				//'survey.view.PVoters.ShowVoters'
				'survey.view.pvoters.ListVoters'
				,{
			name: 'itemselector',
            id: 'itemselector-field',
            store : main.store,
            listeners : {
            	editVoters : function(panel,record){
            		 
            		main.showAddVoters.show(panel);
            	}
            }
            
            
            
		});

		main.panelVoters = Ext.create('survey.view.pvoters.VotersView',{
			url : '/voter/createVoter',
			listeners : {
				refreshOther : function(cmp) {
					 
		            //main.refreshOther();
					main.selectVoters.store.load();
		        }
		    }
			
		
		});
	 	 
		 
	 
		
		
		main.showAddVoters = Ext.create('Ext.window.Window',{
			msgTarget: 'side',
			layout: {
		        type: 'fit',
		        padding: 5
		    },
			modal : true,
			width: 600,
		    minWidth: 350,
		    height: 350,
			closable: true,
		    closeAction: 'hide',
		    showClose : true,
		    maximizable: true,
		    constrain: true,
		    items : [main.panelVoters],
		    listeners:{
                'close':function(win){
                         
                 },
			    'hide':function(win){
	                 
	        }
		    }
		}); 
		 
		
		
		
		 
		
		
		
		main.tbar =  [{
            xtype:'button',
            text: survey.label.create_voters,
            iconCls: 'add16',
            handler: function(bt,ev){
            	main.showAddVoters.show(bt);
            }
        },
        {
            xtype:'button',
            text: survey.label.add_voter_from_contract,
            iconCls: 'add16',
            handler: function(bt,ev){
            	 
            }
        }
        ];
		
		
		
		
		
		
		
		main.items = [main.selectVoters];
		
		this.callParent();
    }
    
});    