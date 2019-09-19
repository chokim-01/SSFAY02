<template>
<v-app>
  <v-content>
    <app-header />
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
  },
  data: () => ({
    //
  }),
};
</script>

<style>
.v-content__wrap {
}

</style>
