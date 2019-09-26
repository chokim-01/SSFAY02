<template>
  <v-layout row wrap>
    <v-flex class="content">
          <v-flex class="title1" xs12 my-4>프로젝트 소개</v-flex>
          <v-flex class="title2" xs12 my-4>네이버 뉴스를 통해 정치적 성향을 알아보고자</v-flex>
          <v-flex class="content1" xs12 my-4>
            개발중...
          </v-flex></br>
          <hr/>
          </br>
          <v-flex class="title2" xs12 my-4>팀원 소개</v-flex>

        <div class="collumns">

          <div class="collumn">
            <div class="head"><span class="headline hl1">박사홍</span>
            </div>
            안녕하세요</p>
            <figure class="figure">
              <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
              <figcaption class="figcaption">하하</figcaption>
            </figure>
          </div>

          <div class="collumn">
            <div class="head"><span class="headline hl1">양동권</span>
            </div>
            안녕하세요</p>
            <figure class="figure">
              <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
              <figcaption class="figcaption">하하</figcaption>
            </figure>
          </div>

          <div class="collumn">
            <div class="head"><span class="headline hl1">박근형</span>
            </div>
            안녕하세요</p>
            <figure class="figure">
              <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
              <figcaption class="figcaption">하하</figcaption>
            </figure>
          </div>

          <div class="collumn">
            <div class="head"><span class="headline hl1">정가영</span>
            </div>
            안녕하세요</p>
            <figure class="figure">
              <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
              <figcaption class="figcaption">하하</figcaption>
            </figure>
          </div>

          <div class="collumn">
            <div class="head"><span class="headline hl1">박홍렬</span>
            </div>
            안녕하세요</p>
            <figure class="figure">
              <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
              <figcaption class="figcaption">하하</figcaption>
            </figure>
          </div>

          <div class="collumn">
            <div class="head"><span class="headline hl1">허정건</span>
            </div>
            안녕하세요</p>
            <figure class="figure">
              <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
              <figcaption class="figcaption">하하</figcaption>
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

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Song+Myung&display=swap');

#newsDetail {
  background-color: #D8D8D8;
}
.collumns{
  margin-left: 2%;
  margin-top: 30px;
}
.collumn
.figure {
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

.collumn
.headline {
    text-align: center;
    line-height: normal;
    font-family: 'Playfair Display', serif;
    display: block;
    margin: 0 auto;

}
.collumn
.headline.hl1 {
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
