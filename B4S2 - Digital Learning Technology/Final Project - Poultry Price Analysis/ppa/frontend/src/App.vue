<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" clipped mobile-breakpoint="640" app>
      <v-list dense shaped>
        <v-list-item v-for="item in items" :key="item.key" :to="item.key" link>
          <v-list-item-icon v-text="item.icon" />
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar clipped-left app color="blue darken-3" dense dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title>🐣家禽價格分析</v-toolbar-title>
    </v-app-bar>
    <v-main>
      <v-container
        fluid
        class="pa-0 overflow-y-auto"
        style="height: calc(100vh - 48px);"
      >
        <transition name="fade" mode="out-in">
          <router-view :key="$route.params.key" />
        </transition>
      </v-container>
    </v-main>
  </v-app>
</template>

<style lang="scss">
// 換頁動畫
.fade-enter-active,
.fade-leave-active {
  transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>

<script>
import { dataItems } from './services/data';

export default {
  name: 'App',
  data: () => ({
    drawer: null,
    items: [{ key: '/', icon: '🏠', title: '首頁' }, ...dataItems],
  }),
};
</script>
