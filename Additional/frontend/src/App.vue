<template>
<v-app>
  <v-content>
    <router-view />
  </v-content>
</v-app>
</template>

<script>
export default {
  name: 'App',
  components: {},
  data: () => ({
    //
  }),
};
</script>

<style>
.v-content__wrap {
  background-color: #d2d2d2;
}

.arrow_box {
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

.arrow_box:after, .arrow_box:before {
	left: 100%;
	top: 50%;
	border: solid transparent;
	content: " ";
	height: 0;
	width: 0;
	position: absolute;
	pointer-events: none;
}

.arrow_box:after {
	border-color: rgba(213, 213, 213, 0);
	border-left-color: #d5d5d5;
	border-width: 10px;
	margin-top: -10px;
}

.arrow_box:before {
	border-color: rgba(24, 28, 31, 0);
	border-left-color: #181c1f;
	border-width: 13px;
	margin-top: -13px;
}
</style>
