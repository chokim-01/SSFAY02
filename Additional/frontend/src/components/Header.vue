<template >
  <html>
  <head>
    <link href='https://fonts.googleapis.com/css?family=Playfair+Display:400,700,900,400italic,700italic,900italic|Droid+Serif:400,700,400italic,700italic' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="styles/newspaper.css">
    <title>Newspaper Style Design Experiment</title>
    <meta name="viewport" content="width=device-width">
  </head>

  <div class="head">
    <div class="headerobjectswrapper">
      <div class="weatherforcastbox"><span style="font-style: italic;">Weatherforcast for the next 24 hours: Plenty of Sunshine</span><br><span>Wind: 7km/h SSE; Ther: 21°C; Hum: 82%</span></div>
      <header> 맥 짚는 AI </header>
    </div>

    <div class="subhead">2019.09.21 published by SSAFY
      <div class="text-xs-center">

   <v-btn color="secondary" @click="MovePage(News)"> News </v-btn>
   <v-btn color="secondary" @click="MovePage(Search)" > Search </v-btn>
   <v-btn color="secondary" @click="MovePage(AboutUs)"> About Us </v-btn>

 </div>





    </div>
  </div>
  </html>

</template>

<script>
export default {

  data () {
      return {
        NowPage: "AboutUs",
      }
    },

    methods: {
    MovePage(location){
      console.log(location)
      this.NowPage = location;
    }
  }
}
</script>

<style lang="css" scoped>

body {
    font-family: 'Droid Serif', serif;
    font-size: 14px;
    color: #2f2f2f;
    background-color: #d2d2d2;
}
header {
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 80px;
    text-transform: uppercase;
    display: inline-block;
    line-height: 72px;
    margin-bottom: 20px;

}
p {
    margin-top: 0;
    margin-bottom: 20px;
}
.head {
    text-align: center;
    position: relative;

}

.headerobjectswrapper {}

.subhead {
    text-transform: uppercase;
    border-bottom: 2px solid #2f2f2f;
    border-top: 2px solid #2f2f2f;
    padding: 12px 0;

}
.weatherforcastbox {
    position: relative;
    width: 12%;
    left: 10px;
    border: 3px double #2f2f2f;
    padding: 10px 15px;
    line-height: 20px;
    display: inline-block;
    margin: 0 50px 20px -360px;
}
</style>
