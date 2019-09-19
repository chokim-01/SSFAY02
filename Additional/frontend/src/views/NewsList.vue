<template>
<v-carousel delimiter-icon="fab fa-apple" prev-icon="fas fa-angle-left" next-icon="fas fa-angle-right">
  <v-carousel-item>
    <v-layout class="content">

      <router-link to="/NewsDetail" class="collumn">
        <div class="head">
          <span class="headline hl3">When darkness overspreads my eyes</span>
          <p><span class="headline hl4">by JOHANN WOLFGANG VON GOETHE</span></p>
        </div>
        <p>When, while the lovely valley teems with vapour around me, and the meridian sun strikes the upper surface of the impenetrable foliage of my trees, and but a few stray gleams steal into the inner sanctuary, I throw myself down among the
          tall
          grass by the trickling stream;<p>and, as I lie close to the earth, a thousand unknown plants are noticed by me: when I hear the buzz of the little world among the stalks, and grow familiar with the countless indescribable forms of the
            insects
            and flies, then I feel the presence of the Almighty, who formed us in his own image, and the breath of that universal love which bears and sustains us, as it floats around us in an eternity of bliss; and then, my friend, when darkness
            overspreads my eyes, and heaven and earth seem to dwell in my soul and absorb its power, like the form of a beloved mistress, then I often think with longing, Oh, would I could describe these conceptions, could impress upon paper all that
            is living so full and warm within me, that it might be the mirror of my soul, as my soul is the mirror of the infinite God!</p>
      </router-link>

      <v-flex class="collumn">
        <div class="head"><span class="headline hl5">Give people courage</span>
          <p><span class="headline hl6">The crowd seemed to grow</span></p>
        </div>
        <p>The sunset faded to twilight before anything further happened. The crowd far away on the left, towards Woking, seemed to grow, and I heard now a faint murmur from it. The little knot of people towards Chobham dispersed. There was scarcely
          an
          intimation of movement from the pit.</p>
        <figure class="figure">
          <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
          <figcaption class="figcaption">Hermine hoping for courage.</figcaption>
        </figure>
        <p>It was this, as much as anything, that gave people courage, and I suppose the new arrivals from Woking also helped to restore confidence. At any rate, as the dusk came on a slow, intermittent movement upon the sand pits began, a movement
          that seemed to gather force as the stillness of the evening about the cylinder remained unbroken. Vertical black figures in twos and threes would advance, stop, watch, and advance again, spreading out as they did so in a thin irregular
          crescent that promised to enclose the pit in its attenuated horns. I, too, on my side began to move towards the pit.</p>
        <p>Then I saw some cabmen and others had walked boldly into the sand pits, and heard the clatter of hoofs and the gride of wheels. I saw a lad trundling off the barrow of apples. And then, within thirty yards of the pit, advancing from the
          direction of Horsell, I noted a little black knot of men, the foremost of whom was waving a white flag.</p>
      </v-flex>

      <v-flex class="collumn">
        <div class="head">
          <span class="headline hl1">May the Force be with you
          </span>
          <p><span class="headline hl2">Let go your conscious self and act on instinct</span></p>
        </div>
        <p>Partially, but it also obeys your commands. Hey, Luke! May the Force be with you. I have traced the Rebel spies to her. Now she is my only link to finding their secret base.</p>
        <figure class="figure">
          <img class="media" src="http://i.giphy.com/4fDWVPMoSyhgc.gif" alt="">
          <figcaption class="figcaption">"This time, let go your conscious self and act on instinct."</figcaption>
        </figure>
        <p>Leave that to me. Send a distress signal, and inform the Senate that all on board were killed. <span class="citation">"Don't under&shy;estimate the Force. I suggest you try it again, Luke."</span> This time, let go your conscious self and
          act on instinct. In my experience, there is no such thing as luck. You're all clear, kid. Let's blow this thing and go home!</p>
        <p>You don't believe in the Force, do you? Partially, but it also obeys your commands. The plans you refer to will soon be back in our hands. As you wish.</p>
      </v-flex>

      <v-flex class="collumn">
        <div class="head">
          <span class="headline hl3">The buzz of the little world </span>
          <p>
            <span class="headline hl4">A thousand unknown plants</span>
          </p>
        </div>
        <p>I should be incapable of drawing a single stroke at the present moment; and yet I feel that I never was a greater artist than now. When, while the lovely valley teems with vapour around me, and the meridian sun strikes the upper surface of
          the impenetrable foliage of my trees, and but a few stray gleams steal into the inner sanctuary, I throw myself down among the tall grass by the trickling stream; and, as I lie close to the earth, a thousand unknown plants are noticed by
          me: when I hear the buzz of the little world among the stalks, and grow familiar with the countless indescribable forms of the insects and flies, then I feel the presence of the Almighty, who formed us in his own image, and the breath</p>
      </v-flex>

      <v-flex class="collumn" @click.stop="dialog = true">
        <div class="head">
          <span class="headline hl1">It wasn't a dream </span>
          <p>
            <span class="headline hl4">by FRANZ KAFKA</span>
          </p>
        </div>
        <p>One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and
          divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. </p>

        <p>His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. "What's happened to me?" he thought. It wasn't a dream. His room, a proper human room although a little too small, lay peacefully
          between its four familiar walls. A collection of textile samples lay spread out on the table - Samsa was a travelling salesman - and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice,
          gilded frame. It showed a lady fitted out with a fur hat and fur boa who sat upright, raising a heavy fur muff that covered the whole of her lower arm towards the viewer. Gregor then turned to look out the window at the dull weather. </p>
      </v-flex>

      <v-dialog v-model="dialog" max-width="290" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-card style="background-color:#D8D8D8;">
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat="flat" @click="dialog = false">
              Disagree
            </v-btn>
            <v-btn color="green darken-1" flat="flat" @click="dialog = false">
              Agree
            </v-btn>
          </v-card-actions>
          <NewsDetail />
        </v-card>
      </v-dialog>
    </v-layout>
  </v-carousel-item>

  <v-carousel-item>
    <v-layout class="content">

      <router-link to="/NewsDetail" class="collumn">
        <div class="head">
          <span class="headline hl3">When darkness overspreads my eyes</span>
          <p><span class="headline hl4">by JOHANN WOLFGANG VON GOETHE</span></p>
        </div>
        <p>When, while the lovely valley teems with vapour around me, and the meridian sun strikes the upper surface of the impenetrable foliage of my trees, and but a few stray gleams steal into the inner sanctuary, I throw myself down among the
          tall
          grass by the trickling stream;<p>and, as I lie close to the earth, a thousand unknown plants are noticed by me: when I hear the buzz of the little world among the stalks, and grow familiar with the countless indescribable forms of the
            insects
            and flies, then I feel the presence of the Almighty, who formed us in his own image, and the breath of that universal love which bears and sustains us, as it floats around us in an eternity of bliss; and then, my friend, when darkness
            overspreads my eyes, and heaven and earth seem to dwell in my soul and absorb its power, like the form of a beloved mistress, then I often think with longing, Oh, would I could describe these conceptions, could impress upon paper all that
            is living so full and warm within me, that it might be the mirror of my soul, as my soul is the mirror of the infinite God!</p>
      </router-link>

      <v-flex class="collumn">
        <div class="head"><span class="headline hl5">Give people courage</span>
          <p><span class="headline hl6">The crowd seemed to grow</span></p>
        </div>
        <p>The sunset faded to twilight before anything further happened. The crowd far away on the left, towards Woking, seemed to grow, and I heard now a faint murmur from it. The little knot of people towards Chobham dispersed. There was scarcely
          an
          intimation of movement from the pit.</p>
        <figure class="figure">
          <img class="media" src="http://i.giphy.com/PW7MoTD2d9pJK.gif" alt="">
          <figcaption class="figcaption">Hermine hoping for courage.</figcaption>
        </figure>
        <p>It was this, as much as anything, that gave people courage, and I suppose the new arrivals from Woking also helped to restore confidence. At any rate, as the dusk came on a slow, intermittent movement upon the sand pits began, a movement
          that seemed to gather force as the stillness of the evening about the cylinder remained unbroken. Vertical black figures in twos and threes would advance, stop, watch, and advance again, spreading out as they did so in a thin irregular
          crescent that promised to enclose the pit in its attenuated horns. I, too, on my side began to move towards the pit.</p>
        <p>Then I saw some cabmen and others had walked boldly into the sand pits, and heard the clatter of hoofs and the gride of wheels. I saw a lad trundling off the barrow of apples. And then, within thirty yards of the pit, advancing from the
          direction of Horsell, I noted a little black knot of men, the foremost of whom was waving a white flag.</p>
      </v-flex>

      <v-flex class="collumn">
        <div class="head">
          <span class="headline hl1">May the Force be with you
          </span>
          <p><span class="headline hl2">Let go your conscious self and act on instinct</span></p>
        </div>
        <p>Partially, but it also obeys your commands. Hey, Luke! May the Force be with you. I have traced the Rebel spies to her. Now she is my only link to finding their secret base.</p>
        <figure class="figure">
          <img class="media" src="http://i.giphy.com/4fDWVPMoSyhgc.gif" alt="">
          <figcaption class="figcaption">"This time, let go your conscious self and act on instinct."</figcaption>
        </figure>
        <p>Leave that to me. Send a distress signal, and inform the Senate that all on board were killed. <span class="citation">"Don't under&shy;estimate the Force. I suggest you try it again, Luke."</span> This time, let go your conscious self and
          act on instinct. In my experience, there is no such thing as luck. You're all clear, kid. Let's blow this thing and go home!</p>
        <p>You don't believe in the Force, do you? Partially, but it also obeys your commands. The plans you refer to will soon be back in our hands. As you wish.</p>
      </v-flex>

      <v-flex class="collumn">
        <div class="head">
          <span class="headline hl3">The buzz of the little world </span>
          <p>
            <span class="headline hl4">A thousand unknown plants</span>
          </p>
        </div>
        <p>I should be incapable of drawing a single stroke at the present moment; and yet I feel that I never was a greater artist than now. When, while the lovely valley teems with vapour around me, and the meridian sun strikes the upper surface of
          the impenetrable foliage of my trees, and but a few stray gleams steal into the inner sanctuary, I throw myself down among the tall grass by the trickling stream; and, as I lie close to the earth, a thousand unknown plants are noticed by
          me: when I hear the buzz of the little world among the stalks, and grow familiar with the countless indescribable forms of the insects and flies, then I feel the presence of the Almighty, who formed us in his own image, and the breath</p>
      </v-flex>
      <v-flex class="collumn" @click.stop="dialog = true">
        <div class="head">
          <span class="headline hl1">It wasn't a dream </span>
          <p>
            <span class="headline hl4">by FRANZ KAFKA</span>
          </p>
        </div>
        <p>One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and
          divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. </p>

        <p>His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. "What's happened to me?" he thought. It wasn't a dream. His room, a proper human room although a little too small, lay peacefully
          between its four familiar walls. A collection of textile samples lay spread out on the table - Samsa was a travelling salesman - and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice,
          gilded frame. It showed a lady fitted out with a fur hat and fur boa who sat upright, raising a heavy fur muff that covered the whole of her lower arm towards the viewer. Gregor then turned to look out the window at the dull weather. </p>
      </v-flex>

      <v-dialog v-model="dialog" max-width="290" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-card style="background-color:#D8D8D8;">
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat="flat" @click="dialog = false">
              Disagree
            </v-btn>
            <v-btn color="green darken-1" flat="flat" @click="dialog = false">
              Agree
            </v-btn>
          </v-card-actions>
          <NewsDetail />
        </v-card>
      </v-dialog>
    </v-layout>
  </v-carousel-item>
</v-carousel>
</template>

<script>
import NewsDetail from "@/components/NewsDetail.vue"

export default {
  name: 'NewsList',
  data() {
    return {
      dialog: false,
      notifications: false,
      sound: true,
      widgets: false
    }
  },
  components: {
    NewsDetail
  }
}
</script>

<style lang="scss" scoped>
.content {
    font-family: 'Droid Serif', serif;
    font-size: 14px;
    line-height: 0;
    word-spacing: -.31em;
    display: inline-block;
    margin-left: 3%;
    box-sizing: content-box !important;
}

.collumn {
    text-decoration: none;
    color: black;
    font-size: 14px;
    line-height: 20px;
    width: 17.5%;
    display: inline-block;
    padding: 0 1%;
    vertical-align: top;
    margin-bottom: 50px;
    transition: all 0.7s;
}

.collumn + .collumn {
    border-left: 1px solid #2f2f2f;
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

.collumn .headline.hl2 {
    font-weight: 400;
    font-style: italic;
    font-size: 24px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl2:before {
    border-top: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 7px;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl2:after {
    border-bottom: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 13px;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl3 {
    font-weight: 400;
    font-style: italic;
    font-size: 36px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl4 {
    font-weight: 700;
    font-size: 12px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl4:before {
    border-top: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 7px;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl4:after {
    border-bottom: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 10px;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl5 {
    font-weight: 400;
    font-size: 42px;
    text-transform: uppercase;
    font-style: italic;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl6 {
    font-weight: 400;
    font-size: 18px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl6:before {
    border-top: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 7px;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl6:after {
    border-bottom: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 10px;
    display: block;
    margin: 0 auto;
}

.collumn .headline.hl7 {
    font-weight: 700;
    font-size: 12px;
    box-sizing: border-box;
    display: block;
    padding: 10px 0;
}

.collumn .headline.hl8 {
    font-weight: 700;
    font-size: 12px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl9 {
    font-weight: 700;
    font-size: 12px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .headline.hl10 {
    font-weight: 700;
    font-size: 12px;
    box-sizing: border-box;
    padding: 10px 0;
}

.collumn .citation {
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    line-height: 44px;
    text-align: center;
    font-weight: 400;
    display: block;
    margin: 40px 0;
    font-feature-settings: "liga", "dlig";
}
.collumn .citation:before {
    border-top: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 16px;
    display: block;
    margin: 0 auto;
}

.collumn .citation:after {
    border-bottom: 1px solid #2f2f2f;
    content: '';
    width: 100px;
    height: 16px;
    display: block;
    margin: 0 auto;
}

.collumn .figure {
    margin: 0 0 20px;
}

.collumn .figcaption {
    font-style: italic;
    font-size: 12px;
}

.media {
    -webkit-filter: sepia(80%) contrast(1) opacity(0.8);
    filter: sepia(80%) grayscale(1) contrast(1) opacity(0.8);
    mix-blend-mode: multiply;
    width: 100%;
}

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

    header {
        max-width: 320px;
        font-size: 60px;
        line-height: 54px;
        overflow: hidden;
    }
}
</style>


<style>
.v-responsive {
  height: auto !important;
}

.v-window {
  height: auto !important;
}

.v-carousel__next .v-btn,
.v-carousel__prev .v-btn {
  color: black !important;
}
</style>
