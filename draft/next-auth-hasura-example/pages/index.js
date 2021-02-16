import Layout from '../components/layout'
import { Media } from "../components/media"
import Text from 'components/text'
export default function HomePage() {
  return (
      <Layout>
      <Media at="xs">Hello mobile!</Media>
      <Media greaterThan="xs">Hello desktop!</Media>
      
      <Text as="h1" size="3">NextAuth.js Example</Text>
      <p>
        This is an example site to demonstrate how to use <a href={`https://next-auth.js.org`}>NextAuth.js</a> for authentication.
      </p>
    </Layout>
  )
}
