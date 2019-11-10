import firebase from 'firebase/app';
import 'firebase/database';

const firebaseConfig = {
  apiKey: 'AIzaSyBj6XrR-xs0cvW3QKsdPxB8vPBVOYiyAeo',
  authDomain: 'amt-tea-corpus.firebaseapp.com',
  databaseURL: 'https://amt-tea-corpus.firebaseio.com',
  projectId: 'amt-tea-corpus',
  storageBucket: 'amt-tea-corpus.appspot.com',
  messagingSenderId: '241227385194',
  appId: '1:241227385194:web:ccccbe92e320bbf47bbd13'
};

export const db = firebase
  .initializeApp({ databaseURL: 'https://amt-tea-corpus.firebaseio.com' })
  .database();
