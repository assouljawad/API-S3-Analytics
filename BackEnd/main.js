import { PutObjectCommand, S3Client } from "@aws-sdk/client-s3";

const client = new S3Client({
  region: "us-east-1",
  credentials: {
    accessKeyId: "",
    secretAccessKey: "",
  },
});
const bucketName = "user-logs-2024";

const fetchData = async () => {
  try {
    console.log("Start fetching Data...");
    const response = await fetch("https://dummyjson.com/users?limit=10");
    const data = await response.json();
    return data.users;
  } catch (err) {
    console.error("Error fetching data:", err);
    throw err;
  }
};

const main = async () => {
  try {
    const users = await fetchData();
    const jsonData = JSON.stringify(users, null, 2);
    const fileName = "user-logs-2024.json";

    const command = new PutObjectCommand({
      Bucket: bucketName,
      Key: fileName,
      Body: jsonData,
    });

    const response = await client.send(command);
    console.log("File uploaded successfully:", response);
  } catch (err) {
    console.error("Error:", err);
  }
};

main();
