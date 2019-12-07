<template>
  <q-page class="q-pa-sm">
    <div class="q-pa-md">
      <MockTable />
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
      filter: ''
    }
  },
  methods: {
    setPageTab: function () {
      if (this.$route.path === '/') {
      }
    }
  }
}
</script>

<style lang="stylus">

</style>
