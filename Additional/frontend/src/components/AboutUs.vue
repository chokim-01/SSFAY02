<template>
  <v-layout row wrap>
    <v-flex class="content">
          <v-flex xs12 class="title1" my-4>팀 소개</v-flex>
          <v-flex xs12 class="title2" my-4>이 프로젝트를 하게 된 이유</v-flex>
          <v-flex xs12 class="content1" my-4>
            dddd
          </v-flex></br></br>
          <hr/>
          </br></br>
          <v-flex xs12 class="title2" my-4>팀원 소개</v-flex>
        <div class="collumns">
          <div class="collumn">
            <div class="head"><span class="headline hl1">Give people courage</span>
            </div>
            The sunset faded to twilight before anything further happened. The crowd far away on the left, towards Woking, seemed to grow, and I heard now a faint murmur from it. The little knot of people towards Chobham dispersed. There was scarcely an
            intimation of movement from the pit.</p>
            <figure class="figure">
              <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
              <figcaption class="figcaption">Hermine hoping for courage.</figcaption>
            </figure>
          </div>
          <div class="collumn">
            <div class="head"><span class="headline hl1">Give people courage</span>
            </div>
            The sunset faded to twilight before anything further happened. The crowd far away on the left, towards Woking, seemed to grow, and I heard now a faint murmur from it. The little knot of people towards Chobham dispersed. There was scarcely an
            intimation of movement from the pit.</p>
            <figure class="figure">
              <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
              <figcaption class="figcaption">Hermine hoping for courage.</figcaption>
            </figure>
          </div>
          <div class="collumn">
            <div class="head"><span class="headline hl1">Give people courage</span>
            </div>
            The sunset faded to twilight before anything further happened. The crowd far away on the left, towards Woking, seemed to grow, and I heard now a faint murmur from it. The little knot of people towards Chobham dispersed. There was scarcely an
            intimation of movement from the pit.</p>
            <figure class="figure">
              <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
              <figcaption class="figcaption">Hermine hoping for courage.</figcaption>
            </figure>
          </div>
          <div class="collumn">
            <div class="head"><span class="headline hl1">Give people courage</span>
            </div>
            The sunset faded to twilight before anything further happened. The crowd far away on the left, towards Woking, seemed to grow, and I heard now a faint murmur from it. The little knot of people towards Chobham dispersed. There was scarcely an
            intimation of movement from the pit.</p>
            <figure class="figure">
              <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
              <figcaption class="figcaption">Hermine hoping for courage.</figcaption>
            </figure>
          </div>
          <div class="collumn">
            <div class="head"><span class="headline hl1">Give people courage</span>
            </div>
            The sunset faded to twilight before anything further happened. The crowd far away on the left, towards Woking, seemed to grow, and I heard now a faint murmur from it. The little knot of people towards Chobham dispersed. There was scarcely an
            intimation of movement from the pit.</p>
            <figure class="figure">
              <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
              <figcaption class="figcaption">Hermine hoping for courage.</figcaption>
            </figure>
          </div>
          <div class="collumn">
            <div class="head"><span class="headline hl1">Give people courage</span>
            </div>
            The sunset faded to twilight before anything further happened. The crowd far away on the left, towards Woking, seemed to grow, and I heard now a faint murmur from it. The little knot of people towards Chobham dispersed. There was scarcely an
            intimation of movement from the pit.</p>
            <figure class="figure">
              <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
              <figcaption class="figcaption">Hermine hoping for courage.</figcaption>
            </figure>
          </div>
        </div>
    </v-flex>
  </v-layout>
</template>

<script>
  export default {
    data () {
      return {

      }
    },
    mounted() {
    }
  }
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Song+Myung&display=swap');

#newsDetail {
  background-color: #D8D8D8;
}

.collumn .figure {
    margin: 0 0 20px;
}

.contentCard {
  height: auto;
}
.title1 {
  overflow: hidden;
  font-family: 'Song Myung', serif;
  font-size: 40px;
  text-align: center;
}

.title2{
  overflow: hidden;
  font-family: 'Song Myung', serif;
  font-size: 28px;
  text-align: center;
}

.content1{
  overflow: hidden;
  font-family: 'Song Myung', serif;
  font-size: 21px;
  text-align: center;
}

.collumn {
    font-size: 14px;
    line-height: 20px;
    width: 16%;
    display: inline-block;
    padding: 0 1%;
    vertical-align: top;
    margin-bottom: 50px;
    transition: all 0.7s;
}

.collumn + .collumn {
    border-left: 1px solid #2f2f2f;
}

.media {
    mix-blend-mode: multiply;
    width: 100%;
}

.collumn .headline {
    text-align: center;
    line-height: normal;
    font-family: 'Playfair Display', serif;
    display: block;
    margin: 0 auto;

}
.collumn .headline.hl1 {
    font-weight: 700;
    font-size: 30px;
    text-transform: uppercase;
    padding: 10px 0;

}

/*MEDIAQUERIES*/
@media only all and (max-width: 1300px) {
    .weatherforcastbox {
        display: none;
    }

}
@media only all and (max-width: 1200px) {
    .collumn {
        width: 31%;
    }

}
@media only all and (max-width: 900px) {
    .collumn {
        width: 47%;
    }

}
@media only all and (max-width: 600px) {
    .collumn {
        width: 100%;
    }
    .collumn + .collumn {
        border-left: none;
        border-bottom: 1px solid #2f2f2f;
    }
}
</style>
