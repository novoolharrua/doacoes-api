import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import './plugins/bootstrap-vue'
import './plugins/axios'

import MaterialKit from "./plugins/material-kit";

Vue.config.productionTip = false;

Vue.use(MaterialKit);

const NavbarStore = {
  showNavbar: false
};

Vue.mixin({
  data() {
    return {
      NavbarStore
    };
  }
});

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");

Vue.component('modal', {
  template: '#modal-template'
})
