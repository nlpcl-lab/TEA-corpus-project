import firebase from "firebase/app";
import "firebase/database";

export const db = firebase
  .initializeApp({ databaseURL: "https://amt-tea-corpus.firebaseio.com" })
  .database();
