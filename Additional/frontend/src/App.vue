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
</style>
