<template>
<v-layout row wrap>
  <v-flex class="positionCenter" xs12 sm8 >
    <div class="wrapper row2 ">
      <div id="container" class="clear">

        <div id="about-us" class="clear">
          <div class="three_fifth first">
            <section id="about-intro" class="clear">
              <div class="panorama"><img class="imgholder" id="about-picture" src="../assets/548x250.gif" alt=""></div>
              <div class="ssafynewstitle">
                <h1 class="introtitle">&nbsp;&nbsp;&nbsp;&nbsp;俟&nbsp;&nbsp;&nbsp;&nbsp;翍&nbsp;日&nbsp;報</h1>
                <p>기다릴 <b>사</b> 날개펼 <b>피</b> <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;일</b> <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;보</b></p>
              </div>
              <b class="introteam">현재는 멈춰있지만 머지않아 날개를 펼 팀 '맥 짚는 AI'입니다.</b>
              <br /><br />
              <h2>Functions</h2>
              <p>⊙ 최근 스포츠이슈들을 노출</p>
              <p>⊙ 뉴스 제목, 키워드, 날짜별 검색</p>
              <p>⊙ 사용자와 대화가 가능한 심심이</p>
              <p>⊙ 뉴스 검색 도우미</p>
              <p>⊙ 기사에 대한 키워드 및 단어 클라우드</p>
              <p>⊙ 댓글에 대한 단어 클라우드</p>
              <p>⊙ 댓글에 대한 시간대 별 작성 수</p>
              <p>⊙ 댓글에 대한 긍/부정 표시 및 전체 수</p>
              <p>⊙ 댓글에 대한 지역감정 포함 여부 표시/숨기기</p>

              <h2>Purpose</h2>
              <p><b>사용자에게 최근 스포츠이슈를 알려주고 기사와 여론에 대한 분석을 제공한다.</b></p>

            </section>
            <br />
            <section id="skillset">
              <div class="fl_left first">
                <h1 class="introtitle">Development Environment</h1>
                <br />
                <h2>Front-End</h2>
                <img class="imgskill" id="about-picture" src="../assets/skills/vue.png" alt="">
                <img class="imgskill" id="about-picture" src="../assets/skills/vuetify.png" alt="">
                <h2>Back-End</h2>
                <img class="imgskill" id="about-picture" src="../assets/skills/python.png" alt="">
                <img class="imgskill" id="about-picture" src="../assets/skills/flask.png" alt="">
                <h2>Development Environment</h2>
                <img class="imgskill" id="about-picture" src="../assets/skills/aws.png" alt="">
                <img class="imgskill" id="about-picture" src="../assets/skills/mysql.png" alt="">
                <img class="imgskill" id="about-picture" src="../assets/skills/tensorflow.png" alt="">


                <p></p>
              </div>
            </section>
          </div>

          <div>
            <section id="team" class="two_fifth">
              <h2>About Us</h2>
              <ul>
                <li v-for="(member, index) in AboutUs" :key="index">
                  <figure><img class="team_picture" :src="member.img" >
                    <figcaption>
                      <p class="team_name">{{member.name}}</p>
                      <p class="team_title">{{member.level}}</p>
                      <p class="team_description">{{member.disc}}</p>
                    </figcaption>
                  </figure>
                </li>
              </ul>
            </section>
          </div>
        </div>
      </div>
    </div>
  </v-flex>
</v-layout>
</template>

<script>

import AboutUs from '@/JS/AboutUs.js'

export default {
  data() {
    return {
      AboutUs: AboutUs
    }
  },
}
</script>

<style scoped>

.positionCenter {
  margin: 0 auto;
}

.imgskill {
  max-width: 150px;
  max-height: 120px;
}

.introtitle {
  font-size: 30px;
  line-height: 1.6em;
}

.ssafynewstitle {
  text-align: center;
}

.one_fifth,
.three_fifth,
.two_fifth {
  display: inline-block;
  float: left;
  margin: 0 0 0 50px;
  list-style: none;
}

.two_fifth {
  width: 372px;

}

.introteam {
    font-size: 20px;
}

.team_picture{
  max-width: 110px;
}

#about-us {
  display: block;
  width: 100%;
  line-height: 2.7em;
}

#about-us #about-intro {
  margin-bottom: 30px;
}

#about-us #about-intro blockquote {
  position: relative;
  margin: 0;
  padding: 0;
}

#about-us #about-intro blockquote p {
  margin: 0;
  padding: 0 0 0 60px;
  font-size: 22px;
  font-style: italic;
  line-height: 1.6em;
}

#about-us #about-intro blockquote p span {
  position: absolute;
  top: 0;
  left: 0;
  font-size: 120px;
  line-height: .8em;
}

#about-us #skillset {
  margin-bottom: 0;
}

#about-us #skillset .fl_left:first-child {
  margin-left: 0;
}

#about-us #skillset .fl_left li {
  margin-top: 5px;
}

#about-us #skillset .fl_left li:first-child {
  margin-top: 0;
}

#about-us #team {
  margin-bottom: 0;
}

#team h2 {
  margin-bottom: 10px;
}

#about-us #team ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

#about-us #team ul li {
  display: block;
  margin: 10px 0 0 0;
}

#about-us #team ul li:first-child {
  margin-top: 0;
}

#about-us #team ul li figcaption {
  float: right;
  width: 250px;
}

#about-us #team ul li figcaption p {
  margin: 0;
  padding: 0;
}

#about-us #team ul li figure figcaption .team_name {
  font-weight: bold;
}

#about-us #team ul li figure figcaption .team_title {
  font-size: 11px;
  line-height: normal;
}

#about-us #team ul li figure figcaption .team_description {
  margin-top: 10px;
  line-height: 1.4em;
}


@media (max-width: 600px) {
  #about-picture {
    width: 90%;
  }

  .one_fifth,
  .two_fifth,
  .three_fifth,
  .four_fifth {
    display: inline-block;
    float: left;
    margin: 0 0 0 20px;
    list-style: none;
  }

  #about-us #team ul li figcaption {
    float: left;
    width: 220px;
  }
}

</style>
