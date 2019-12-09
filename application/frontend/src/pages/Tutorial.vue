<template>
  <div class="q-pa-md">
  <Strong style="font-size: 200%;"> {{ tutorial.title }} </Strong>

    <!-- ---------- IMAGE CODEBLOCK ---------- -->
    <div
      class="row justify-start"
      style="margin:20px;"
    >
      <div class="col-2">
        <q-img
          :src="'https://placeimg.com/500/300/nature?t=' + Math.random()"
          style="
            max-width: 200px;
            height: 150px;
            align: left;
            vertical-align: top;
            border: solid black 1px;
          "
        />
      </div>

      <div class="col q-py-md">
        <strong class="text-h4">
          Description
        </strong>
        <br>
        <div class="q-px-lg q-my-sm">
          {{ tutorial.description }}
        </div>
      </div>
    </div >

    <!-- ---------- MATERIAL LIST CODEBLOCK ---------- -->
    <div>
      <q-expansion-item
        expand-separator
        icon="list"
        label="Material list"
        style="max-width: 400px; padding: 10px;"
        default-opened
      >
        <q-list dense bordered padding class="rounded-borders">
          <q-item
            v-for="(list, ind) in lists"
            :key="ind"
          >
            <q-item-section>
              {{ ind + 1 }}.  {{ list }}
            </q-item-section>
          </q-item>
        </q-list>
      </q-expansion-item>
    </div>

    <!-- ---------- STEP CODEBLOCK ---------- -->
    <div class="q-pa-md" style="max-width: 650px;">
      <strong>Steps</strong>
      <q-list>
        <q-item
          v-for="(step, ind) in steps"
          :key="ind"
        >
          <q-item-section style="max-width:20px">
            {{ ind + 1 }}.
          </q-item-section>

          <q-item-section top thumbnail class="q-ml-none">
            <img src="https://cdn.quasar.dev/img/mountains.jpg">
          </q-item-section>
          <q-item-section>
            <q-item-label style="padding:10px;">{{ step }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </div>
     <div>
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
    axios.get(`http://54.153.68.76:5000/api/tutorial/${this.$q.localStorage.getItem('__diyup__username')}/${this.obj_uuid}`)
      .then(res => {
        this.data = res.data.tutorial
        console.log(this.data)
      })
  },
  data () {
    return {
      obj_uuid: null,
      data: [],
      tutorial: {
        title: 'Title',
        url: 'img',
        description: 'some description'
      },
      lists: [
        'None'
      ],
      steps: null
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
    }
  }
}
</script>
