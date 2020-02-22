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

type PublisherType implements SpriklNode {
  name: String!
  address: String!
  id: ID!
  allBooks: [BookType!]
}

type Query {
  book(id: ID!): BookType
}

interface SpriklNode {
  id: ID!
}
""".lstrip()
    )
