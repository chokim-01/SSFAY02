import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    SERVER_URL: 'http://localhost:5000',
    searchKey: "",
    searchCat: "",
    searchChk: false
  },
});
