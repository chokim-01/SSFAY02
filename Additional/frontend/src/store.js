import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
//    SERVER_URL: "http://13.125.116.42:5000",
    SERVER_URL: " http://localhost:5000/",
    searchKey: "",
    searchCategory: "",
    searchLabel: [{
      all: "전체",
      title: "제목",
      tag: "태그",
      date: "날짜"
    }],
    searchCheck: false,
    oneNewsInfo: [""]
  },
});
