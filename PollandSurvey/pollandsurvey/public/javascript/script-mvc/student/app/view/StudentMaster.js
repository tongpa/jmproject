Ext.define('School.view.StudentMaster', {

    extend: 'Ext.form.Panel',
    alias: 'widget.StudentMaster',
    config: {},
    constructor: function (config) {
        this.initConfig(config);
        return this.callParent(arguments);
    },
    
    clearForm: function () {
        this.getForm().getFields().each(function (field) {
            field.validateOnChange = false;
            field.setValue('');
            field.resetOriginalValue();
        });
    },
    initComponent: function () {
        var required = '<span style="color:red;font-weight:bold" data-qtip="Required">*</span>';

        Ext.apply(this, {
            id: 'StudentMasterId',
            title: 'Student Information',
            resizable: false,
            collapsible: true,
            bodyPadding: '5',
            buttonAlign: 'center',
            border: false,
            trackResetOnLoad: true,
            layout: {
                type: 'vbox'
            },
            defaults: {
                xtype: 'textfield',
                msgTarget: 'side',
                labelAlign: 'top',
                labelStyle: 'font-weight:bold'
            },
            items: [{
                xtype: 'fieldcontainer',
                layout: 'hbox',
                defaultType: 'textfield',
                width: '100%',
                fieldDefaults: {
                    labelAlign: 'top',
                    labelStyle: 'font-weight:bold'
                },
                items: [{
                    fieldLabel: 'Id',
                    name: 'Id',
                    readOnly: true,
                    width: 35
                }, 
                {
                    fieldLabel: 'First Name',
                    flex: 1,
                    name: 'firstName',
                    afterLabelTextTpl: required,
                    margin: '0 0 0 5',
                    allowBlank: false
                },
                {
                    name: 'middleName',
                    width: 150,
                    margin: '0 0 0 5',
                    fieldLabel: 'Middle Name:'
                },
                {
                    fieldLabel: 'Last Name',
                    flex: 1,
                    margin: '0 0 0 5',
                    name: 'lastName'
                }]
            },
                {
                    xtype: 'datefield',
                    fieldLabel: 'Date of Birth',
                    name: 'birthDate'
                },
                {
                    xtype: 'textfield',
                    fieldLabel: 'Address',
                    width: '100%',
                    name: 'address1'
                },
                {
                    xtype: 'textfield',
                    hideLabel: true,
                    name: 'address2',
                    width: '100%',
                    fieldLabel: 'address2'
                },
                {
                    xtype: 'textfield',
                    fieldLabel: 'City',
                    width: '100%',
                    name: 'city'
                },
                {
                    xtype: 'textfield',
                    fieldLabel: 'state',
                    width: '100%',
                    name: 'state'
                },
                {
                	xtype : 'UserMasterView',
                	id : 'UserMasterView'
                }],
            buttons: [
                { text: 'Create',
                    itemId: 'btnCreate'
                },
                { text: 'Read Data',
                    itemId: 'btnLoad'
                },

                { text: 'Update',
                    itemId: 'btnUpdate'
                },
                { text: 'Delete',
                    itemId: 'btnDelete'
                },
                { text: 'Reset',
                    itemId: 'btnReset'
                },
                { text: 'Clear',
                    itemId: 'btnClear'
                }]
        });
        this.callParent(arguments);
    }
});