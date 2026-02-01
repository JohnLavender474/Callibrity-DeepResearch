export async function uploadFile(
  profileId: string,
  file: File
): Promise<void> {
  await uploadToStorage(profileId, file);
  await embedDocument(profileId, file);
}


async function uploadToStorage(
  profileId: string,
  file: File
): Promise<void> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(
    `/api/storage/collections/${profileId}/blobs`,
    {
      method: 'POST',
      body: formData,
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(
      `Failed to upload file to storage: ${error.detail || response.statusText}`
    );
  }
}


async function embedDocument(
  profileId: string,
  file: File
): Promise<void> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(
    `/api/embeddings/collections/${profileId}/upload`,
    {
      method: 'POST',
      body: formData,
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(
      `Failed to embed document: ${error.detail || response.statusText}`
    );
  }
}
