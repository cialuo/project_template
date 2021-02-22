odoo.define(
    "student.payslip.action_recalculate_paid_status",
    function (require) {
        "use strict";
        /**
         * Button 'Create' is replaced by Custom Button
         **/

        var core = require("web.core");
        var ListController = require("web.ListController");
        ListController.include({
            renderButtons: function ($node) {
                this._super.apply(this, arguments);
                if (this.$buttons) {
                    console.log("im here");
                    this.$buttons.on(
                        "click",
                        ".o_list_button_recalculate_paid_status",
                        this._action_def.bind(this)
                    );
                }
            },

            //--------------------------------------------------------------------------
            // Define Handler for new Custom Button
            //--------------------------------------------------------------------------

            /**
             * @private
             * @param {MouseEvent} event
             */
            _action_def: function (e) {
                var self = this;
                var active_id = this.model.get(this.handle).getContext()[
                    "active_ids"
                ];
                var model_name = this.model.get(this.handle).getContext()[
                    "active_model"
                ];
                this._rpc({
                    model: "student.payslip",
                    method: "js_python_method",
                    args: [model_name, active_id],
                }).then(function (result) {
                    console.log("result", result);
                    // self.do_action(result);
                });
            },
        });
    }
);
