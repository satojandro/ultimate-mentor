import { json, JSONValue, TypedMap } from "@graphprotocol/graph-ts";
import { Project } from "../generated/schema";

export function handleData(data: JSONValue): void {
  let projects = data.toArray();

  for (let i = 0; i < projects.length; i++) {
    let projectData = projects[i].toObject();
    let showcaseUrlValue = projectData.get("showcaseUrl");

    if (showcaseUrlValue) {
      let showcaseUrl = showcaseUrlValue.toString();
      let project = new Project(showcaseUrl); // Use showcaseUrl as the unique ID

      // Helper function to safely get string values
      function getString(key: string): string | null {
        let value = projectData.get(key);
        return value && !value.isNull() ? value.toString() : null;
      }

      project.name = getString("name")!;
      project.tagline = getString("tagline");
      project.description = getString("description");
      project.howItsMade = getString("howItsMade");
      project.githubUrl = getString("githubUrl");
      project.projectUrl = getString("projectUrl");
      project.showcaseUrl = showcaseUrl;

      project.save();
    }
  }
}
