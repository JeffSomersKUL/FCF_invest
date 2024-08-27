export async function handleFetch(url, options = {}, returnOn400) {
  let response;
  let errorMessageResponse;
  try {
    response = await fetch(url, options);
  } catch (error) {
    console.log(error);
    return;
  }
  if (response.status >= 300 && !(response.status == 400 && returnOn400)) {
    const responseText = await response.text();
    try {
      const jsonResponse = JSON.parse(responseText);
      errorMessageResponse = jsonResponse.error.message;
    } catch (error) {
      errorMessageResponse = responseText;
    }
    console.log(errorMessageResponse);
    return;
  }
  let json;
  try {
    const headers = options.headers;
    if (headers["Content-type"] == "text/html") {
      json = await response.text();
    } else {
      json = await response.json();
    }
  } catch (error) {
    console.log(error);
    return;
  }
  return json;
}
