/**
 * form controller extend, add save and exit
 */
odoo.define("funenc.FormControllerExt", function (require) {
  "use strict";

  var FormController = require("web.FormController");

  FormController.include({
    _onButtonClicked: function (ev) {
      // stop the event's propagation as a form controller might have other
      // form controllers in its descendants (e.g. in a FormViewDialog)
      ev.stopPropagation();
      var self = this;
      var def;

      this._disableButtons();

      function saveAndExecuteAction() {
        return self
          .saveRecord(self.handle, {
            stayInEdit: true,
          })
          .then(function () {
            // we need to reget the record to make sure we have changes made
            // by the basic model, such as the new res_id, if the record is
            // new.
            var record = self.model.get(ev.data.record.id);
            return self._callButtonAction(attrs, record);
          });
      }

      function SaveAndExit() {
        return self
          .saveRecord(self.handle, {
            stayInEdit: true,
          })
          .then(function () {
            // we need to reget the record to make sure we have changes made
            // by the basic model, such as the new res_id, if the record is
            // new.
            var record = self.model.get(ev.data.record.id);
            var action = { type: "ir.actions.act_window_close", infos: record };
            return self.do_action(action, {});
          });
      }

      var attrs = ev.data.attrs;
      if (attrs.confirm) {
        def = new Promise(function (resolve, reject) {
          Dialog.confirm(this, attrs.confirm, {
            confirm_callback: saveAndExecuteAction,
          }).on("closed", null, resolve);
        });
      } else if (attrs.special === "cancel") {
        def = this._callButtonAction(attrs, ev.data.record);
      } else if (attrs.special === "save_and_exit") {
        def = SaveAndExit();
      } else if (!attrs.special || attrs.special === "save") {
        // save the record but don't switch to readonly mode
        def = saveAndExecuteAction();
      } else {
        console.warn("Unhandled button event", ev);
        return;
      }

      // Kind of hack for FormViewDialog: button on footer should trigger the dialog closing
      // if the `close` attribute is set
      def
        .then(function () {
          self._enableButtons();
          if (attrs.close) {
            self.trigger_up("close_dialog");
          }
        })
        .guardedCatch(this._enableButtons.bind(this));
    },
  });

  return FormController;
});
