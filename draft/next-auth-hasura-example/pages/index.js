import Layout from '../components/layout'
import { Media } from "../components/media"

export default function HomePage() {
  return (
      <Layout>
      <Media at="xs">Hello mobile!</Media>
      <Media greaterThan="xs">Hello desktop!</Media>
      
      <h1>NextAuth.js Example</h1>
      <p>
        This is an example site to demonstrate how to use <a href={`https://next-auth.js.org`}>NextAuth.js</a> for authentication.
      </p>
    </Layout>
  )
}
