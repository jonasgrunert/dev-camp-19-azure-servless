const axios = require("axios");

if (!process.env.TEXT_ANALYTICS_SUBSCRIPTION_KEY) {
  throw new Error("No Subscription Key");
}

if (!process.env.TEXT_ANALYTICS_ENDPOINT) {
  throw new Error("No Endpoint");
}
const subscriptionKey = process.env.TEXT_ANALYTICS_SUBSCRIPTION_KEY;
const endpoint = process.env.TEXT_ANALYTICS_ENDPOINT;
const sentiment_url = endpoint + "/text/analytics/v2.1/sentiment";

module.exports = async function(context, req) {
  const token = req.headers.authorization;
  if (!token) {
    context.res = {
      body: JSON.stringify({
        code: "Unauthorized",
        message: "No Authorization header found"
      }),
      headers: {
        "Content-Type": "application/json"
      },
      code: 403
    };
    return;
  }
  const language = req.params.language || "en";
  const res = await axios.get(
    `https://graph.facebook.com/v5.0/me/posts?fields=message&access_token=${token}`
  );
  const documents = res.data.data
    .filter(i => !!i.message)
    .map((x, i) => ({
      id: i,
      language: language,
      text: x.message
    }));
  const sentiments = await axios.post(sentiment_url, {
    headers: {
      "Ocp-Apim-Subscription-Key": subscriptionKey
    },
    data: {
      documents
    }
  });
  if (sentiments.errors.length != 0) {
    context.res = {
      status: 500,
      body: JSON.stringify(sentiments.errors),
      headers: { "Content-Type": "application/json" }
    };
    return;
  }
  const data = sentiments.documents.map((d, i) => ({ [documents[i].text]: d }));
  if (req.query.name || (req.body && req.body.name)) {
    context.res = {
      body: JSON.stringify(data)
    };
  }
};
