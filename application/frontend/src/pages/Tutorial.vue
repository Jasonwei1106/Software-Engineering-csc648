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
      <!-- <Comment style="margin-top:25px"/> -->
    </div>
  </div>
</template>

<script>
// import Comment from '../pages/Comments'

export default {
  created () {
    if (this.$q.localStorage.has('__diyup__donetutorial')) {
      this.tutorial = this.$q.localStorage.getItem('__diyup__donetutorial')
      this.lists = this.$q.localStorage.getItem('__diyup__donematerial')
      this.steps = this.$q.localStorage.getItem('__diyup__donestep')
      this.$q.localStorage.remove('__diyup__donetutorial')
      this.$q.localStorage.remove('__diyup__donematerial')
      this.$q.localStorage.remove('__diyup__donestep')
    } else if (this.$q.localStorage.has('__diyup__entry')) {
      this.tutorial = this.$q.localStorage.getItem('__diyup__entry')
      this.tutorial.description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    }
  },
  data () {
    return {
      tutorial: {
        title: 'Title',
        url: 'img',
        description: 'some description'
      },
      lists: null,
      steps: null
    }
  }
  // components: {
  //   Comment
  // }
}
</script>
