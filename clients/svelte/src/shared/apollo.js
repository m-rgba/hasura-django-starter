import ApolloClient from "apollo-client";
import { InMemoryCache } from "apollo-cache-inmemory";
import { WebSocketLink } from "apollo-link-ws";
import { split } from "apollo-link";
import { HttpLink } from "apollo-link-http";
import { getMainDefinition } from "apollo-utilities";
import { token } from './auth.js'

const cache = new InMemoryCache();

const wsLink = new WebSocketLink({
    uri: "ws://localhost:8080/v1/graphql",
    options: {
        lazy: true,
        reconnect: true,
        connectionParams: async () => {
            const accessToken = await token();
            return {
                headers: {
                    Authorization: token ? `Bearer ${accessToken}` : "",
                },
            }
        },
    },
});

const httpLink = new HttpLink({
  uri: "http://localhost:8080/v1/graphql",
  headers: async () => {
    const accessToken = await token();
        return {
            Authorization: token ? `Bearer ${accessToken}` : "",
        }
    }
});

const link = split(
  ({ query }) => {
    const { kind, operation } = getMainDefinition(query);
    return kind === "OperationDefinition" && operation === "subscription";
  },
  wsLink,
  httpLink
);

export const client = new ApolloClient({
  link,
  cache
});
