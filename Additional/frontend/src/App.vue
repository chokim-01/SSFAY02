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

</style>
