"use strict";
const mfrc522 = require("mfrc522-rpi");

mfrc522.initWiringPi(0);
let continueReading = true;

//# This loop keeps checking for chips. If one is near it will get the UID and authenticate
console.log("scanning...");
console.log("Please put chip or keycard in the antenna inductive zone!");
console.log("Press Ctrl-C to stop.");

const defaultUrl = "github.com";
let payload = process.argv[2] ? process.argv[2] : defaultUrl;

while (continueReading) {
  //# reset card
  mfrc522.reset();

  //# Scan for cards
  let response = mfrc522.findCard();
  if (!response.status) {
      continue;
  }

  //# Get the UID of the card
  response = mfrc522.getUid();
  if (!response.status) {
      console.log("UID Scan Error");
      continue;
  }
  //# If we have the UID, continue
  const uid = response.data;

  // add 0xFE to end of message
  payload = payload + "þ";
  // character to be inserted after NDEF header
  let firstChar = payload.slice(0, 1).charCodeAt(0);
  let stringArray = chunkSubstr(payload.slice(1), 4);

  // NDEF message headers
  let data = [0x03, 0x44, 0xD1, 0x01];
  console.log(mfrc522.getDataForBlock(4));
  mfrc522.writeDataToBlock(4, data);
  // 0x04 = https://
  data = [0x40, 0x55, 0x04, firstChar];
  console.log(mfrc522.getDataForBlock(5));
  mfrc522.writeDataToBlock(5, data);

  const startBlock = 6;
  for (var i = startBlock; i < (startBlock + stringArray.length); i++){
    // must read page before writing
    mfrc522.getDataForBlock(i);
    let binPayload = string2Bin(stringArray[i-startBlock]);
    console.log(`Block ${i}`);
    console.log(binPayload);
    mfrc522.writeDataToBlock(i, binPayload);
    console.log(mfrc522.getDataForBlock(i).splice(0, 4));
  }
  continueReading = false;
  console.log("finished successfully!");
}

function string2Bin(str) {
  var result = [];
  for (var i = 0; i < str.length; i++) {
    // result.push(str.charCodeAt(i).toString(10));
    result.push(str.charCodeAt(i));
  }
  return result;
}

function chunkSubstr(str, size) {
  var numChunks = Math.ceil(str.length / size),
      chunks = new Array(numChunks);

  for(var i = 0, o = 0; i < numChunks; ++i, o += size) {
    chunks[i] = str.substr(o, size);
  }

  return chunks;
}