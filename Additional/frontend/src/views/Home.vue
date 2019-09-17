<template>
  <html>
    <Header />
    <NewsList />
  </html>
</template>

<script>
import Header from '@/components/Header.vue'
import NewsList from '@/components/NewsList.vue'

export default {
  name: 'home',
  components: {
    Header,
    NewsList,
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>
