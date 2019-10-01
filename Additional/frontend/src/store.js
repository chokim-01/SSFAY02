import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    SERVER_URL: "http://13.125.116.42:5000",
    searchKey: "",
    searchCategory: "",
    searchCheck: false,
    oneNewsInfo: [""]
  },
});
