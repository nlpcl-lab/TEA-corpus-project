import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '@/components/HelloWorld';
import Acceptability from '@/components/Acceptability';
import Entailment from '@/components/Entailment';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/acceptability/:id',
      name: 'Acceptability',
      component: Acceptability
    },
    {
      path: '/entailment/:id',
      name: 'Entailment',
      component: Entailment
    }
  ]
});
