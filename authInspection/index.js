module.exports = async function (context, req) {

    if (req.headers) {
        context.res = {
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(req.headers)
        };
    }
    else {
        context.res = {
            status: 400,
            body: "No headers found"
        };
    }
};