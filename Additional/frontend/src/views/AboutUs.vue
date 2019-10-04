<template>
<v-layout row wrap>
  <v-flex class="positionCenter" xs12 sm8>
    <div class="wrapper row2 ">
      <div id="container" class="clear">

        <div id="about-us" class="clear">
          <div class="three_fifth first">
            <section id="about-intro" class="clear">
              <div class="panorama"><img class="imgholder" id="about-picture" src="../assets/548x250.gif" alt=""></div>
              <p>설명설명</p>
            </section>

            <section id="skillset">
              <div class="fl_left first">
                <h2>개발 환경</h2>
                <p>언어</p>
                <p>프레임워크</p>
              </div>
            </section>
          </div>

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

.one_fifth,
.two_fifth,
.three_fifth,
.four_fifth {
  display: inline-block;
  float: left;
  margin: 0 0 0 50px;
  list-style: none;
}

.two_fifth {
  width: 372px;
}

.four_fifth {
  width: 764px;
}

.team_picture{
  max-width: 110px;
}

#about-us {
  display: block;
  width: 100%;
  line-height: 1.6em;
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
