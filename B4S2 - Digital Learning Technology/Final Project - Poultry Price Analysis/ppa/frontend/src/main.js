import '@mdi/font/css/materialdesignicons.css';
import '@/assets/fonts/style.scss';
import '@/styles/global.scss';

import Vue from 'vue';
import App from '@/App.vue';
import router from '@/router';
import vuetify from '@/plugins/vuetify';

Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
