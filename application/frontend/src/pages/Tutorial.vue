<template>
  <div
    class="q-pa-md shadow-2"
    style="
      width: 98%;
      max-width: 1000px;
      margin: 1em auto;
      border-radius: 3px;
    "
  >
    <div align="center">
      <Strong style="font-size: 200%;">{{ data.title }}</Strong>
      <q-separator color="red" />
    </div>

    <!-- ---------- IMAGE CODEBLOCK ---------- -->
    <div class="row q-pa-md">
      <div class="col-3">
        <q-img
          placeholder-src="https://placeimg.com/500/300/nature"
          :src="'https://placeimg.com/500/300/nature=t' + Math.random()"
          style="
            height: 150px;
            align: left;
            vertical-align: top;
            border: solid black 1px;
          "
        />
        <div
          align="center"
          class="q-mt-xs bg-primary text-white"
          style="border-radius: 3px;"
        >
          <strong>Level of Difficulty:</strong>
          {{ data.author_difficulty }}
        </div>
      </div>

      <div class="col q-pl-md">
        <strong class="text-h4">
          Description
          <q-separator color="red" />
        </strong>
        <div class="q-px-lg q-my-sm">
          {{ data.description }}
        </div>
      </div>
    </div >

    <!-- ---------- MATERIAL LIST CODEBLOCK ---------- -->
    <div>
      <q-expansion-item
        expand-separator
        icon="list"
        label="Material list"
        style="padding: 10px;"
        default-opened
      >
        <q-list dense bordered padding class="rounded-borders">
          <q-item
            v-for="(list, ind) in lists"
            :key="ind"
          >
            <q-item-section>
              {{ ind + 1 }}.  {{ list.name }}
            </q-item-section>
          </q-item>
        </q-list>
      </q-expansion-item>
    </div>

    <!-- ---------- STEP CODEBLOCK ---------- -->
    <div class="q-pa-md">
      <strong class="text-h4">
        Steps
        <q-separator color="red" />
      </strong>
      <q-list>
        <q-item
          v-for="(step, ind) in data.steps"
          :key="ind"
        >
          <q-item-section style="max-width:20px">
            {{ ind + 1 }}.
          </q-item-section>

          <q-item-section top thumbnail class="q-ml-none">
            <img src="https://cdn.quasar.dev/img/mountains.jpg">
          </q-item-section>
          <q-item-section>
            <q-item-label style="padding:10px;">{{ step.content }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </div>

    <div class="q-pb-lg q-pl-md">
      <div>
        <strong>Current Tutorial Rating:</strong>

        <q-rating
          readonly
          class="q-pl-sm"
          size="2em" icon="thumb_up"
          :value="data.rating === 'None' ? 5.0 : Number(data.rating)"
        />
      </div>

      <div>
        <strong>Rate this Tutorial: </strong>

        <q-rating
          class="q-pl-sm"
          size="2em" icon="thumb_up"
          v-model="userRate"
          v-if="$q.localStorage.has('__diyup__signedIn')"
          @input="invokeRating"
        />
      </div>
    </div>

    <q-separator color="black" />

    <div class="q-pa-md">
      <strong class="text-h4">
        Comment Section
        <q-separator />
      </strong>
      <Comment :obj_uuid="obj_uuid" style="margin-top:25px"/>
    </div>
  </div>
</template>

<script>
import Comment from '../components/Comments'
import axios from 'axios'

export default {
  created () {
    this.updateObjUuid()
    axios.all([
      axios.get(`http://54.67.109.241:5000/api/tutorial/${this.obj_uuid}/get`),
      axios.get(`http://54.67.109.241:5000/api/items/${this.obj_uuid}/get`)])
      .then(([res1, res2]) => {
        this.data = res1.data.tutorial
        this.lists = res2.data.items
      })
  },
  data () {
    return {
      userRate: 0,
      obj_uuid: null,
      data: [],
      lists: [
        'None'
      ]
    }
  },
  components: {
    Comment
  },
  watch: {
    $route: 'updateObjUuid'
  },
  methods: {
    updateObjUuid: function () {
      this.obj_uuid = this.$route.params.uuid
    },
    invokeRating: function () {
      let domain = 'http://54.67.109.241:5000'
      let path = `${domain}/api/rate/${this.data.uuid}/score/create`
      let headers = {
        'x-access-token': this.$q.localStorage.getItem('__diyup__signedIn')
      }

      axios.post(path, {
        rating: Number(this.userRate)
      }, { headers }).then(() => {
        this.$q.notify({
          message: '<div align="center">Thank you for rating!<div>',
          color: 'positive',
          html: true
        })
      })
    }
  }
}
</script>
