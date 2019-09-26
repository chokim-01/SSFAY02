import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    SERVER_URL: window.location.href,
    searchKey: "",
    searchCat: "",
    searchChk: false
  },
});
