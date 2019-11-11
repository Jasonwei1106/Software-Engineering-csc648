<template>
  <q-page class="q-pa-sm">
    <div class="q-pa-md">
      <q-btn
        outline
        label="Create a new project"
        @click="gotopost"
        v-if="isHidden"
      />
      <!-- <q-card>
        <q-tabs
          inline-label
          align="justify"
          class="bg-purple text-white shadow-2"
          v-model="pageTab"
          :breakpoint="0"
        >
          <q-route-tab exact name="hot" label="What's Hot?" to="/hot" no-caps />
          <q-route-tab exact name="new" label="What's New?" to="/new" no-caps />
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="pageTab" animated>
          <q-tab-panel name="hot">
            <div class="text-h6">What's Hot</div>
            <MockTable :filter = this.filter />
          </q-tab-panel>

          <q-tab-panel name="new">
            <div class="text-h6">What's New</div>
            <MockTable />
          </q-tab-panel>
        </q-tab-panels>

      </q-card> -->
      <MockTable :filter = this.filter />
    </div>
  </q-page>
</template>

<script>
import MockTable from '../components/MockTable'

export default {
  name: 'PageIndex',
  components: {
    MockTable
  },
  created () {
    this.setPageTab()
  },
  beforeUpdate () {
    this.setPageTab()
  },
  data () {
    return {
      filter: '',
      pageTab: '',
      isHidden: false
    }
  },
  methods: {
    setPageTab: function () {
      if (this.$route.path === '/') {
        this.pageTab = 'hot'
      }
    },
    gotopost: function () {
      let item = this.$q.localStorage.has('__diyup__signedIn')
      console.log(item)
      if (item) {
        this.$router.push({ path: '/post' })
      }
    }
  }
}
</script>

<style lang="stylus">

</style>
