<template>
<v-app>
  <app-header />
  <v-content>
    <router-view />
  </v-content>
</v-app>
</template>

<script>
import mainHeader from "@/components/Header.vue";

export default {
  name: "App",
  components: {
    "app-header": mainHeader,
  }
};
</script>

<style>
#newsCommentPage i {
  transform: scale(0.6);
}
#realNewsTitle li {
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.arrow_box_right {
	position: relative;
	background: #d5d5d5;
	border: 2px solid #181c1f;
  display: inline-block;
  padding: 10px;
  float: right;
  clear: both;
  margin-top: 3px;
  margin-right: 15px;
}

.arrow_box_right:after, .arrow_box:before {
	left: 100%;
	top: 50%;
	border: solid transparent;
	content: " ";
	height: 0;
	width: 0;
	position: absolute;
	pointer-events: none;
}

.arrow_box_right:after {
	border-color: rgba(213, 213, 213, 0);
	border-left-color: #d5d5d5;
	border-width: 10px;
	margin-top: -10px;
}

.arrow_box_right:before {
	border-color: rgba(24, 28, 31, 0);
	border-left-color: #181c1f;
	border-width: 13px;
	margin-top: -13px;
}

.arrow_box_left {
	position: relative;
	background: #d5d5d5;
	border: 2px solid #181c1f;
  display: inline-block;
  padding: 10px;
  float: left;
  clear: both;
  margin-top: 3px;
  margin-left: 15px;
}

.arrow_box_left:after, .arrow_box:before {
	right: 100%;
	top: 50%;
	border: solid transparent;
	content: " ";
	height: 0;
	width: 0;
	position: absolute;
	pointer-events: none;
}

.arrow_box_left:after {
	border-color: rgba(213, 213, 213, 0);
	border-right-color: #d5d5d5;
	border-width: 10px;
	margin-top: -10px;
}

.arrow_box_left:before {
	border-color: rgba(24, 28, 31, 0);
	border-right-color: #181c1f;
	border-width: 13px;
	margin-top: -13px;
}
</style>
