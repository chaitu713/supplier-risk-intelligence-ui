import { useQuery } from "@tanstack/react-query";

import {
  getEsgRecords,
  getSuppliers,
  getTransactions,
  type DatasetKey,
  type DatasetRecord,
} from "../../../api/datasets";

const datasetQueryMap: Record<DatasetKey, () => Promise<DatasetRecord[]>> = {
  suppliers: getSuppliers,
  esg: getEsgRecords,
  transactions: getTransactions,
};

export function useDatasetExplorer(dataset: DatasetKey) {
  return useQuery({
    queryKey: ["datasets", dataset],
    queryFn: datasetQueryMap[dataset],
  });
}
