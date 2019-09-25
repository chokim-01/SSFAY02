import Vue from 'vue'
import App from './App.vue'
import { store } from './store'
import router from './router'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import '@fortawesome/fontawesome-free/css/all.css'
import Swimlane from 'vue-swimlane'

Vue.use(Swimlane)
Vue.use(Vuetify)


Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: function (h) { return h(App) }
}).$mount('#app')
