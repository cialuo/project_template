odoo.define('hello_world_view.HelloWorldView', function(require) {
    "use strict";
    var BasicView = require('web.BasicView');
    var BasicModel = require('web.BasicModel');
    var BasicRenderer = require('web.BasicRenderer');
    var BasicController = require('web.BasicController');
    var viewRegistry = require('web.view_registry');
    var core = require('web.core');
    var QWeb = core.qweb;
    var HelloWorldController = BasicController.extend({
        init: function(parent, model, renderer, params) {
            this._super.apply(this, arguments);
            this.test = model.test
            console.log('controller model', model);
            console.log('controller renderer', renderer);
            console.log('controller params', params);
        }
    });
    var HelloWorldModel = BasicModel.extend({
        init: function(parent, params) {
            this._super.apply(this, arguments);
            this.test = 'test'
            console.log('model params', params)
        },
    });
    var HelloWorldRenderer = BasicRenderer.extend({
        className: 'o_hello_world_view',
        async _renderView() {
            console.log('data', this.state.data)
            console.log('state', this.state);
            window.data = this.state.data ? this.state.data : []
            this.$el.html(QWeb.render('hello_world_view', { tem: 'dungdung ' }));
        },
        init: function(parent, state, params) {
            this._super.apply(this, arguments);
            console.log('renderer attrs', this.arch);
            console.log('renderer state', state);
            console.log('renderer this.state', this.state)
            console.log('renderer params', params)
            this.test = params.test
            window.data = this.state.data ? this.state.data.data : []
                // this.loadParams.displayContacts = this.arch.attrs.display_contacts;
        },

    });

    var HelloWorldView = BasicView.extend({
        init: function(viewInfo, params) {
            var self = this;
            this._super.apply(this, arguments);
            console.log('params', params)
            console.log('this', this)
            this.rendererParams.test = 'world'
        },
        config: _.extend({}, BasicView.prototype.config, {
            Model: HelloWorldModel,
            Controller: HelloWorldController,
            Renderer: HelloWorldRenderer,
        }),
        viewType: 'hello_world',
    })
    viewRegistry.add('hello_world', HelloWorldView);

    return HelloWorldView;
});

/*
odoo.define('hello_world_view.HelloWorldController', function (require) {
    "use strict";
    
    
    var AbstractController = require('web.AbstractController');
    
    var HelloWorldController = AbstractController.extend({});
    
    return HelloWorldController;
    
});
*/