from tests.test_app.test_app.schema import schema


def test_schema():
    assert (
        str(schema)
        == """
schema {
  query: Query
}

type AuthorType implements SpriklNode {
  firstName: String!
  lastName: String!
  email: String!
  id: ID!
}

type BookType implements SpriklNode {
  title: String!
  id: ID!
  publisher: PublisherType
  allAuthors: [AuthorType!]
}

type BookTypeConnection {
  pageInfo: PageInfo!
  edges: [BookTypeEdge]!
  totalCount: Int!
}

type BookTypeEdge {
  node: BookType
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type PublisherType implements SpriklNode {
  name: String!
  address: String!
  id: ID!
  allBooks: [BookType!]
}

type Query {
  book(id: ID!): BookType
  books(before: String, after: String, first: Int, last: Int): BookTypeConnection
}

interface SpriklNode {
  id: ID!
}
""".lstrip()
    )
